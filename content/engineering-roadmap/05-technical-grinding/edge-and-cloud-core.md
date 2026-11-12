# Edge and cloud: understand the data journey

**Level: Intermediate** · Start with the Year 1 roadmap if these ideas are unfamiliar.

Status: Draft | Independent review pending

A cloud service runs on remotely managed infrastructure. An edge service places processing at a distributed network location closer to a user or device in some deployments. Whether it improves latency depends on the full request path and system design.

The blueprint’s advanced example receives ESP32 telemetry, checks fields and a message signature, converts a raw measurement and forwards it to another service.

## Trace the stages

**Device → HTTPS request → validation → authentication → conversion → forwarding → storage**

| Decision | Why it matters | Limitation to explain |
| --- | --- | --- |
| Per-device secrets | Limits the effect of one exposed credential | Provisioning, rotation and revocation still matter |
| HMAC signature | Checks message integrity and shared-secret authentication | Does not itself stop replay |
| Timestamp window | Rejects messages outside an allowed time range | Repeats inside the window remain possible |
| Per-device counter | Can help detect repeated messages | Needs consistent stored state and reset rules |
| Background forwarding | Can shorten the immediate device response | Acceptance does not guarantee eventual storage |
| ADC conversion | Turns a raw count into an estimated voltage | Calibration and hardware assumptions affect accuracy |

## Advanced exercise

Use simulated messages first. Test malformed data, unknown device, invalid signature, old timestamp and duplicate message. Decide what an “accepted” response promises. If delivery must survive failures, design durable queuing and retries rather than assuming background work provides that guarantee.

The original code remains in the supplied blueprint PDF and archived transcription. It is not presented as tested runnable code. A standalone implementation needs a separate technical review and verification before publication as a working project.

---
Source basis: Campus to Corporate blueprint, Version 4. Adapted for this guide; additions and pathway suggestions require review.
