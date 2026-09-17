#requires -Version 7
<#
fit-video-bgm.ps1
Fit a music track to a video's exact length and mux them together.

Why this exists
---------------
YuE2 has no exact-duration control. Its ComfyUI node derives the token budget as
max_duration * 25 fps; if the budget runs out the model is cut off mid-phrase and
the track ends "hanging". Capping max_duration to the video length is therefore
wrong: it causes the hang.

Correct recipe:
  1. Generate with a generous max_duration (e.g. 90s) so the model writes a real
     ending (end token) instead of being truncated.
  2. Match the video length here, in post, without touching the musical ending.

Strategy
--------
  audio slightly longer  -> pitch-preserving atempo speeds it up to exactly the
                            video length (intro AND ending survive).
  audio much longer      -> keep the song's natural ending, drop N seconds from
                            the head.
  audio shorter          -> loop it to the video length.
  always                 -> short fade-out so the end sounds intentional.

Usage
-----
  pwsh scripts/fit-video-bgm.ps1 -Video <video.mp4> -Audio <bgm.flac>
  pwsh scripts/fit-video-bgm.ps1 -Video v.mp4 -Audio bgm.flac -Out out.mp4 -FadeSeconds 3
#>
param(
    [Parameter(Mandatory)] [string]$Video,
    [Parameter(Mandatory)] [string]$Audio,
    [string]$Out,
    [double]$FadeSeconds = 2.0,
    [double]$MaxAtempo = 0.20
)

$ErrorActionPreference = 'Stop'

$ff = "E:\AI\sound-plan\tools\ffmpeg-shared\ffmpeg-master-latest-win64-gpl-shared\bin\ffmpeg.exe"
$fp = "E:\AI\sound-plan\tools\ffmpeg-shared\ffmpeg-master-latest-win64-gpl-shared\bin\ffprobe.exe"
if (-not (Test-Path -LiteralPath $ff)) { throw "ffmpeg tidak ada: $ff" }
if (-not (Test-Path -LiteralPath $Video)) { throw "video tidak ada: $Video" }
if (-not (Test-Path -LiteralPath $Audio)) { throw "audio tidak ada: $Audio" }

function Get-Duration([string]$Path) {
    [double](& $fp -v error -show_entries format=duration -of csv=p=0 -- $Path)
}

$vdur = Get-Duration $Video
$adur = Get-Duration $Audio
if ($vdur -le 0 -or $adur -le 0) { throw "durasi tidak valid (video=$vdur audio=$adur)" }

if (-not $Out) {
    $dir  = Split-Path -Parent $Video
    $base = [IO.Path]::GetFileNameWithoutExtension($Video)
    $Out  = Join-Path $dir "$base`_bgm.mp4"
}

$fadeSt = [Math]::Max(0.0, $vdur - $FadeSeconds)
$ratio  = $adur / $vdur
$t      = ('{0:0.###}' -f $vdur)
$fade   = ('afade=t=out:st={0:0.###}:d={1:0.###}' -f $fadeSt, $FadeSeconds)

Write-Host ("video {0:N2}s | audio {1:N2}s | ratio {2:N3}" -f $vdur, $adur, $ratio)

if ($adur -ge $vdur -and $ratio -le (1.0 + $MaxAtempo)) {
    Write-Host "-> atempo (pitch-preserving) -> tepat sepanjang video"
    & $ff -y -i $Audio -i $Video `
        -filter_complex "[0:a]atempo=$ratio,$fade[a]" `
        -map 1:v -map "[a]" -c:v copy -c:a aac -b:a 320k `
        -t $t -movflags +faststart $Out
}
elseif ($adur -gt $vdur) {
    $skip = $adur - $vdur
    Write-Host ("-> buang {0:N2}s dari AWAL (ending asli dipertahankan) + fade" -f $skip)
    & $ff -y -ss ('{0:0.###}' -f $skip) -i $Audio -i $Video `
        -filter_complex "[0:a]$fade[a]" `
        -map 1:v -map "[a]" -c:v copy -c:a aac -b:a 320k `
        -t $t -movflags +faststart $Out
}
else {
    Write-Host "-> loop BGM sampai sepanjang video + fade"
    & $ff -y -stream_loop -1 -i $Audio -i $Video `
        -filter_complex "[0:a]$fade[a]" `
        -map 1:v -map "[a]" -c:v copy -c:a aac -b:a 320k `
        -t $t -movflags +faststart $Out
}

if ($LASTEXITCODE -ne 0) { throw "ffmpeg gagal (exit $LASTEXITCODE)" }

# Guard: make sure the audio actually landed (a FLAC with a stale total-sample
# header can make -ss seek past the real data and yield an audio-less output).
$astream = & $fp -v error -select_streams a:0 -show_entries stream=codec_name -of csv=p=0 $Out
if (-not $astream) {
    Remove-Item -LiteralPath $Out -ErrorAction SilentlyContinue
    throw "output tidak punya stream audio - periksa durasi/header file audio input"
}

$rdur = Get-Duration $Out
Write-Host ("selesai -> {0}  ({1:N2}s, audio={2})" -f $Out, $rdur, $astream)
