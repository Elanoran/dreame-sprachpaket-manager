# Example: a "Jarvis"-style voice

[jarvis-lines.txt](jarvis-lines.txt) is a 593-line announcement script -
every real (non-silent) entry in the sound catalog, rewritten as a
dry, formal, Iron-Man-butler-style line. It's plain text, in the
format the app's *Import Texts from File* expects. No audio is
included here, on purpose - see below.

## Why there's no audio in this repo

The original version of this pack was voiced with an AI clone of a
specific, real, working actor's voice, made from a public interview
clip. That's a fun idea for a private hobby project on your own
robot. It is a different matter to put the resulting audio in a
public repository for anyone to download and install:

* A person's voice is generally protected as part of their likeness
  (personality rights in the EU/UK, right of publicity in much of the
  US), separately from copyright. A clone convincing enough to be a
  good Jarvis is, by the same measure, convincing enough to be
  mistaken for the real person.
* Private, personal use is a very different exposure than public,
  unbounded redistribution - this project draws that same line for
  the built-in dialect packs (see [LICENSE-AUDIO.md](../../LICENSE-AUDIO.md):
  no use as training material, no resale), and a named actor's cloned
  voice is a stricter case than a licensed stock voice.

So: the script (the actual creative work) is here to reuse. The
cloned celebrity audio isn't, and won't be added.

## How to voice this script legally

Whichever of these you pick, the workflow in the app is the same:
**Custom Voices → Create Custom Pack ... → copy an existing dialect →
Import Texts from File → pick `jarvis-lines.txt`**, then generate
audio for it. See [docs/Eigene-Stimmen.md](../../docs/Eigene-Stimmen.md)
for the full walkthrough of that screen.

- **Windows Text-to-Speech.** Free, offline, built into the app.
  Pick any installed English voice. Not a dramatic butler, but zero
  licensing questions of any kind.
- **ElevenLabs.** Also built into the app. Use one of their stock
  voices (their terms allow this kind of use) rather than their voice
  cloning feature on a real person's recording.
- **Your own voice, or someone who's consented.** Record it yourself,
  or ask a friend / a voice actor who explicitly agrees. This is the
  one case where cloning is unambiguously fine, because the person
  whose voice it is has said yes.
- **A hired/licensed voice actor or synth voice**, if you want a
  specific character read professionally - check the license covers
  this exact use (personal, on a physical device you own).
- **Cloning a public figure's voice with a tool like ComfyUI +
  Chatterbox,** if that's what you want to experiment with: keep it
  private. Generate it for your own robot, don't publish the audio
  files, and don't distribute a pack built from it. That keeps the
  fun part (a good voice on your own vacuum) without turning it into
  something you're redistributing on someone else's behalf.

None of this is legal advice - if you're unsure about a specific case
(e.g. a commercial voice actor's license terms), read the license or
ask a lawyer, not this README.
