class MultipleFunctions():
    def Subfields():    
        print("Sub-fields in AI are:")
        values=["Machine Learning", "Neural Networks", "Vision", "Robotics", "Speech Processing", "Natural Language Processing"]
        for Values in values:
            print(Values)
    
    def OddEven():
        number= int(input("Enter a number:"))
        if ((number%2) ==1):
            print(number, "is an Odd Number")
        else:
            print(number, "is an Event Number")

    def Elegible():
        gender=input("Your gender:")
        age=int(input("Your age:"))
        if ((gender == "Male" or gender == "male" and age >= 21) or (gender == "Female" or gender == "female" and age >= 18)):
            response="ELIGIBLE"
        else:
            response="NOT ELIGIBLE"
            
        return response

    def percentage():
        Subject1=98
        Subject2=87
        Subject3=95
        Subject4=95
        Subject5=93
        Total= Subject1+Subject2+Subject3+Subject4+Subject5
        Percentage= Total/500*100
        print("Subject1=", Subject1)
        print("Subject2=", Subject2)
        print("Subject3=", Subject3)
        print("Subject4=", Subject4)
        print("Subject5=", Subject5)
        return Percentage

    def triangle():
        Height=32
        Breadth=34
        Areaformula= (Height*Breadth)/2
        AreaofTriangle= Areaformula
        Height1=2
        Height2=4
        Breadth2=4
        Perimeterformula= Height1+Height2+Breadth2
        PerimeterofTriangle= Perimeterformula
        print("Height:", Height)
        print("Breadth:", Breadth)
        print("Area formula: (Height*Breadth)/2", )
        print("Area of Triangle:", AreaofTriangle)
        print("Height1:", Height1)
        print("Height2:", Height2)
        print("Breadth:", Breadth2)
        print("Perimeter of Triangle:", PerimeterofTriangle)
