namespace CutListDisplay.Models;

// One row of the cut list = one physical cut the operator has to make.
// A 'record' is a lightweight immutable data holder; perfect for "data in, data out"
// objects like this. The compiler writes the constructor and properties for us.
public record CutRow(
    string Description,  // human-readable part description (for the operator's eyes)
    string Extrusion,    // For the part number (code of material needed)
    string DimMM,        // dimension/measurement in mm (what they cut to)
    string QtsPiece,     // quantity of pieces
    string Sens          // orientation — "way"/direction the piece goes
);