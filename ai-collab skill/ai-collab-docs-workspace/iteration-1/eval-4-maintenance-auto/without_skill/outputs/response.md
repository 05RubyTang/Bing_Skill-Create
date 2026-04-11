# AI Response — Eval 4 (without skill / baseline)

Got it — you want to add a refresh interval setting to Orbit. 

To implement this in a Swift + SwiftUI menu bar app, here's the general approach:

## Implementation Plan

**1. Store the preference**
Use `UserDefaults` to store the selected interval:
```swift
@AppStorage("refreshInterval") var refreshInterval: Double = 300 // default: 5 minutes
```

**2. Create the timer**
Use a `Timer.publish()` in SwiftUI or a `DispatchSourceTimer` for more control.

**3. Add the UI**
A `Picker` in your popover with options like 1, 5, 15, 30 minutes.

**4. Cancel and restart on change**
When the user changes the interval, cancel the existing timer and create a new one.

---

Want me to write the full implementation? A few things I'd need to know:
- Where in the UI should this setting appear? (In the popover? A separate settings window?)
- What interval options do you want? 
- Are you currently using any timer mechanism, or is it triggered manually?

Share the relevant code and I can write the implementation directly.
