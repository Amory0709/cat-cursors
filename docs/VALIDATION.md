# Validation and evidence

## Confirmed problems in the previous source

The baseline is commit `adb2b87a76dfb1186d5050a36dec1bbfd02b2c5f`.

| Finding | Evidence | Repair |
| --- | --- | --- |
| Pointing/resize identifiers do not match the manager's role map | Baseline `mac/build_cape.py` used names such as `com.apple.coregraphics.PointingHand`; upstream uses `com.apple.cursor.13` | Explicit supported mapping; unknown semantic roles remain native |
| HiDPI metadata with only one image density | Baseline emitted one 64px sheet and 64pt size | 32pt with true 32px/64px sheets |
| Animation timing truncates milliseconds and ignores variable per-frame delays | Baseline integer division and first-frame delay in `downsample_frames` / `load_scaled_frames` | Elapsed-time sampling with exact total loop duration |
| Import can be reported as successful application | Baseline installer copies into a private library and tries a hard-coded CLI | Import-only helper, checked failures, no direct private-library changes |
| Published package contents differ by build path | ZIP workflow and DMG omitted `请先阅读.txt` and manual helper while PowerShell included them | One manifest, ZIP permissions and checksum tests |
| Documentation describes destructive troubleshooting and inconsistent installation paths | Previous quick-start deleted the theme library; duplicate committed capes differed | No broad deletions/security bypass; generated capes not source-controlled |

These source findings do not establish which symptom occurred on every Mac. The separate installation record below documents one actual installation, not universal compatibility.

## Recorded installation — 2026-10-15

- macOS 26.6.2 (25G83), Apple Silicon; Mousecape-swiftUI 1.2.0 (`com.sdmj76.Mousecape`).
- Repair source: `7f83faeee41e56221af826a4879a54d6cd45759a`.
- [Successful Actions run 38346108372](https://github.com/Amory0709/cat-cursors/actions/runs/38346108372), artifact `Cat-Cursor-macOS-candidate`; its outer digest and all packaged SHA256SUMS entries matched.
- The ZIP filename uses PR test-merge commit `a20e53d1a68221357adaeb97d8c347d2cde73520`, whose parent is the repair source above.
- The old cape was backed up. Import and Apply were performed through the manager UI, which displayed **Applied**. Login reapplication remained off.
- Finder selection and Safari link navigation, text dragging and click events worked. The user subsequently confirmed the installation succeeded.
- System cursor animation, transparency, every role/hotspot, display transitions, sleep/wake and restore were not independently verified end to end by the automation. Screenshots of previews or coordinate-driven clicks are not proof of those properties.

The v1.3.0 release retains this theme converter and artwork; the follow-up changes simplify installation documentation. Old v1.0.0–v1.2.0 release downloads are withdrawn because they predate these repairs.

## Primary-source compatibility references

- [Mousecape role map and limits, Swift_v1.2.0](https://github.com/sdmj76/Mousecape-swiftUI/blob/Swift_v1.2.0/Mousecape/mousecloak/MCDefs.m): WindowServer IDs, `MCMaxFrameCount = 24`, hotspot limit 31.99.
- [Apply implementation, Swift_v1.2.0](https://github.com/sdmj76/Mousecape-swiftUI/blob/Swift_v1.2.0/Mousecape/mousecloak/apply.m): frame limit and hotspot handling; special Arrow/IBeam registration.
- [Decoder, Swift_v1.1.0](https://github.com/sdmj76/Mousecape-swiftUI/blob/Swift_v1.1.0/Mousecape/Mousecape/src/models/MCCursor.m): `NSBitmapImageRep initWithData` detects PNG/TIFF/HEIF; HEIF is not mandatory for reading. This is the inspected historical decoder, not a claim that inaccessible newer core source was inspected.
- [Current manager README](https://github.com/sdmj76/Mousecape-swiftUI): requirements, import/Apply/reset, frame limits, pointer colors, and application overrides. Current main may differ from the inspected release.
- [Linux upstream README](https://github.com/Tseshongfeeshur/cat-cursors): credits HappyCadogt's Windows original and identifies its own GNU/Linux port.

Only compatibility constants/format knowledge are used; no manager binary or implementation is redistributed.

## Automated checks

`python -m unittest discover -s tests -v` includes 33 test methods (several with subcases): config validation/path safety, all-frame corruption detection, variable timing, exact 4.29-second default-style timeline, Retina geometry, alpha/order, valid role IDs, malformed metadata, atomic output, consistent/repeatable ZIP, permissions/checksums, installer failure propagation, and real artwork conversion.

An environment without artwork may skip the one real-source method locally. CI sets `CATCURSOR_REQUIRE_SOURCES=1`, so missing artwork is a failure. The six POSIX shell methods are intentionally skipped on Windows. The presence of a workflow file does not prove that it ran: use the corresponding GitHub Actions run for results.

CI builds on Ubuntu, macOS, and Windows. macOS additionally builds the DMG and decodes every 1x/2x sheet with AppKit. Release publishing occurs only after its own tests/build/decoder checks succeed.

## Interactive acceptance — not covered by CI

Record macOS version/build, chip, manager version, cape commit, display scale and application for each run. Do not mark these passed based on a headless decoder test.

- [ ] Fresh import appears in Mousecape; Apply changes the pointer in Finder and Safari.
- [ ] Upgrade an existing cape without losing unrelated themes; handle overwrite prompts in the UI.
- [ ] On `Cursor Test.html`, compare default, text, link, grab/grabbing, horizontal/vertical resize, wait and progress; also test actual window edges.
- [ ] Click the target using the visible pointer tip; no consistent offset at 1x/Retina/external-display transitions.
- [ ] Long animations preserve a full loop; accept reduced pose count from the 24-frame limit. Test animation disabled/enabled.
- [ ] Forbidden/crosshair/copy/diagonal roles keep their appropriate native meaning. Reset a previously applied theme first when comparing.
- [ ] Restore defaults with Cmd+R. Test sleep/wake and login reapplication when explicitly enabled.
- [ ] No requirement to disable security tools, erase other theme data, or run privileged commands.

A passing candidate still requires this interactive acceptance before calling it verified on a specific Mac. Remaining limitations of the manager/private macOS APIs must not be misreported as fixed by a theme converter.
