// Headless AppKit decoder test; does NOT apply cursors to WindowServer.
import AppKit
import Foundation

func check(_ condition: Bool, _ message: String) throws {
    if !condition {
        throw NSError(domain: "CatCursorValidation", code: 1,
                      userInfo: [NSLocalizedDescriptionKey: message])
    }
}

do {
    try check(CommandLine.arguments.count == 2, "Usage: swift verify_cape.swift file.cape")
    let data = try Data(contentsOf: URL(fileURLWithPath: CommandLine.arguments[1]))
    guard let cape = try PropertyListSerialization.propertyList(from: data, options: [], format: nil) as? [String: Any],
          let cursors = cape["Cursors"] as? [String: [String: Any]], !cursors.isEmpty else {
        throw NSError(domain: "Invalid cape", code: 1)
    }
    var checked = 0
    for (name, cursor) in cursors {
        guard let count = cursor["FrameCount"] as? Int,
              let width = cursor["PointsWide"] as? NSNumber,
              let height = cursor["PointsHigh"] as? NSNumber,
              let representations = cursor["Representations"] as? [Data] else {
            throw NSError(domain: "Invalid cursor: \(name)", code: 1)
        }
        try check((1...24).contains(count), "Invalid frame count: \(name)")
        try check(representations.count == 2, "Missing Retina representation: \(name)")
        for (index, bytes) in representations.enumerated() {
            guard let image = NSBitmapImageRep(data: bytes) else {
                throw NSError(domain: "AppKit cannot decode \(name)", code: 1)
            }
            let scale = index + 1
            try check(image.pixelsWide == width.intValue * scale, "Width: \(name)")
            try check(image.pixelsHigh == height.intValue * scale * count, "Height: \(name)")
            try check(image.hasAlpha, "Missing transparency: \(name)")
            checked += 1
        }
    }
    print("AppKit decoded \(checked) sprite sheets for \(cursors.count) roles. Interactive Apply remains a manual check.")
} catch {
    FileHandle.standardError.write(Data("\(error)\n".utf8))
    exit(1)
}
