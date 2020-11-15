print([0]*3)
class Fract :
    def __init__(self,nom,denom):
        self.nom=nom
        self.denom=denom
    def __str__(self):
        return str(self.nom)+'/'+str(self.denom)
    def __add__(self,other):
        new_denom=self.denom*other.denom
        new_nom=self.nom*other.denom+other.nom*self.denom
        return Fract(new_nom, new_denom)
    def __sub__(self,other):
        new_denom = self.denom * other.denom
        new_nom = self.nom * other.denom - other.nom * self.denom
        return new_nom, new_denom

a=Fract(1,2)
b=Fract(3,4)

print(a+b)
class Student :
    def __init__(self,name,surname,age,course):
        self.name=name
        self.surname=surname
        self.age=age
        self_course=course
class Group:
    def __init__(self,name):
        self.name=name
        self.students=[]
    def add_student (self,student):
        self.students.append(Student)
    def __str__(self):
        return str(self.students)
    def get_students(self):
        return self.students[:]
    def sub_student(self,student):
        ind=self.students.index
        sub_student=self.students.pop(ind)
        return sub_student
group_1=Group('19FPL')
student_1=Student('Tania','Romanova',56,36)
group_1.add_student(student_1)
print(group_1)
a=group_1.sub_student(student_1)