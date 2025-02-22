import comtypes.client
import numpy as np
import matplotlib.pyplot as plt

try:
    myETABSObject = comtypes.client.GetActiveObject("CSI.ETABS.API.ETABSObject")
    SapModel = myETABSObject.SapModel
    print("✅ Connected to ETABS successfully.")
except Exception as e:
    print(f"❌ Failed to connect to ETABS: {e}")
    exit()

ret = SapModel.FrameObj.GetNameList(0, [])
NumberFrames = ret[0]  # Number of beams
FrameNames = ret[1]    # List of beam names

print(f"📌 Number of beams: {NumberFrames}")

# Select load case for shear force extraction
SapModel.Results.Setup.DeselectAllCasesAndCombosForOutput()
SapModel.Results.Setup.SetCaseSelectedForOutput("Dead")  # Example: Dead Load

# Dictionary to store shear results
ShearResults = {}

# Extract shear force for each beam

for frame in FrameNames:
    Label = ""
    Story = ""

    
    ret = SapModel.FrameObj.GetLabelFromName(frame, Label, Story)
    Label_Story = ret
    if "B" in ret[0] :

        NumberResults = 0
        Obj = []
        ObjSta = []
        Elm = []
        LoadCase = []
        StepType = []
        StepNum = []
        P = []  # Axial Force
        V2 = []  # Shear Force in direction 2
        V3 = []  # Shear Force in direction 3 (Required)
        T = []  # Torsion
        M2 = []  # Moment around axis 2
        M3 = []  # Moment around axis 3

        ret = SapModel.Results.FrameForce(frame, 0 , NumberResults, Obj , ObjSta , Elm, LoadCase, StepType, StepNum, P, V2, V3, T, M2, M3)
# print(ret)
    
        if ret[-1] == 0:  # If data is retrieved successfully
            ShearResults[frame] = {
            "Position": np.linspace(-1, 1, len(ret[1])),  # Relative position along beam
            "Shear": np.array(ret[-6]),  # Shear force (V2)
            "Label": Label_Story
            }





for frame, data in ShearResults.items():
    position = data["Position"]
    shear = data["Shear"]
    label = data["Label"]
    
    plt.figure(figsize=(8, 6))
    plt.plot(position, shear, marker='o', linestyle='-', color='g', label="Shear V2")
    plt.fill_between(position, shear, where=(position > 0), color='blue', alpha=0.3, label="Negative Shear")
    plt.fill_between(position, shear, where=(position < 0), color='r', alpha=0.3, label="Positive Shear")
    plt.axhline(0, color='black', linewidth=1)
    plt.xlabel("Normalized Position along Beam")
    plt.ylabel("Shear Force (V2)")
    plt.title(f"Shear Diagram for {label[0]} {label[1]}")
    plt.legend()
    plt.grid(True)
    plt.show()