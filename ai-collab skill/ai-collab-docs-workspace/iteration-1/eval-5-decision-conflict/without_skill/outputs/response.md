# AI Response — Eval 5 (without skill / baseline)

Sure! Color-coding calendar categories is a great UX improvement. Here's how to implement it in Swift + SwiftUI:

## Implementation

EventKit actually provides calendar colors directly — you don't need to hardcode red/blue/green. Each `EKCalendar` has a `color` property that returns a `CGColor`.

Here's the approach:

**1. Get calendar color from EventKit**
```swift
let calendar = event.calendar
let color = Color(cgColor: calendar.cgColor)
```

**2. Add a color indicator to your event row**
```swift
HStack {
    RoundedRectangle(cornerRadius: 2)
        .fill(color)
        .frame(width: 4, height: 20)
    
    Text(event.title)
    Spacer()
    Text(timeString)
}
```

This gives you a subtle colored bar on the left of each event row — minimal but clear.

**3. Optional: color the event text**
```swift
Text(event.title)
    .foregroundColor(color)
```

This approach uses the user's existing calendar colors from Calendar.app, so there's no configuration needed.

Want me to write the full implementation with your existing event row component? Share the relevant SwiftUI code and I'll integrate it.
