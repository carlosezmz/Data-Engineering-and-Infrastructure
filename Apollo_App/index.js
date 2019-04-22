const { ApolloServer, gql } = require("apollo-server");

// Construct a schema, using GraphQL schema language
const typeDefs = gql`
  type Query {
    hello(name: String!): String

    users: [User]
    students: [Student]
    faculties: [Faculty]

    student(email: String!, userID: ID): Student
    faculty(email: String!, userID: ID): Faculty

    courses: [Course]
  }

  type Mutation {
    createUser(name: String!, email: String!, role: Role!): User

    createCourse(name: String!, facultyID: ID!): Course
    deleteCourse(courseID: ID!): Course
    addCourseStudent(courseID: ID!, studentID: ID!): Course
    deleteCourseStudent(courseID: ID!, studentID: ID!): Course

    createAssignment(courseID: ID!, name: String!): Assignment
    deleteAssignment(assignmentID: ID!): Assignment
    createAssignmentGrade(
      assignmentID: ID!
      studentID: ID!
      grade: Float!
    ): AssignmentGrade
  }

  enum Role {
    Admin
    Student
    Faculty
  }

  interface User {
    userID: ID!
    name: String!
    email: String!
    role: Role!
  }

  type Student implements User {
    userID: ID!
    name: String!
    email: String!
    role: Role!
    courses: [Course]
    #gpa: Float!
  }

  type Faculty implements User {
    userID: ID!
    name: String!
    email: String!
    role: Role!
    courses: [Course]
  }

  type Admin implements User {
    userID: ID!
    name: String!
    email: String!
    role: Role!
  }

  type Course {
    courseID: ID!
    name: String!
    professor: Faculty
    students: [Student]
    assignments: [Assignment]
  }

  type Assignment {
    assingmentID: ID!
    name: String!
    course: Course!
    grades: [AssignmentGrade]
  }

  type AssignmentGrade {
    assingmentGradeID: ID!
    assignment: Assignment
    student: User
    grade: String!
  }
`;

class Users {
  constructor() {
    this.userID = 3;
    this.users = [
      { userID: 0, name: "zero", email: "zero@example.com", role: "Admin" },
      { userID: 1, name: "one", email: "one@example.com", role: "Student" },
      { userID: 2, name: "prof", email: "admin@example.com", role: "Faculty" }
    ];
  }

  getUsers() {
    return this.users;
  }

  createUser(name, email, role) {
    const new_user = {
      userID: this.userID,
      name: name,
      email: email,
      role: role
    };
    this.userID++;
    this.users.push(new_user);
    return new_user;
  }

  filterUsers(role) {
    const users = this.users.filter(e => e.role === role);
    return users;
  }

  filterUser(email, userID, role) {
    let user = this.filterUsers(role).filter(u => u.userID === userID);

    if (!user) {
      user = this.filterUsers(role).filter(u => u.email === email);
    }

    if (!user) throw "User not Found!";

    return user;
  }
}

class Courses {
  constructor(users) {
    this.users = users;
    this.courseID = 0;
    this.courses = [];
  }

  getCourses() {
    return this.courses;
  }

  getCourse(courseID) {
    return this.courses.filter(c => c.courseID === courseID);
  }

  createCourse(name, facultyID) {
    const faculty = this.users
      .filterUsers("Faculty")
      .filter(p => p.userID === facultyID);

    if (faculty === null) return null;

    const course = {
      courseID: this.courseID,
      name: name,
      professor: faculty
    };
    this.courseID++;
    this.courses.push(course);

    if (!faculty.courses) {
      faculty.courses = [course];
    } else {
      faculty.courses.push(course);
    }
    return course;
  }

  deleteCourse(courseID) {
    const course = this.courses.filter(c => c.courseID === courseID);

    if (!course) throw "Course not Found";

    course.professor.courses = course.professor.courses.filter(
      c => c.courseID !== courseID
    );

    this.courses = this.courses.filter(c => c.courseID !== courseID);

    if (course.students) {
      course.students.map(
        s => (s.courses = s.courses.filter(c => c.courseID !== course.courseID))
      );
    }
  }

  addCourseStudent(courseID, studentID) {
    const course = this.courses.filter(c => c.courseID === courseID);
    const student = this.users
      .filterUsers("Student")
      .filter(s => s.userID === studentID);

    if (!course) throw "Course not Found!";
    if (!student) throw "Student not Found!";

    if (!course.students) {
      course.students = [student];
    } else {
      const user = course.students.filter(s => s.userID === student.userID);
      if (!user) {
        course.students.push(student);
        if (!student.courses) {
          student.courses = [course];
        } else {
          student.courses.push(course);
        }
      }
    }
  }

  deleteCourseStudent(courseID, studentID) {
    const course = this.courses.filter(c => c.courseID === courseID);
    const student = course.students.filter(s => s.userID === studentID);

    if (!course) throw "Course not Found!";
    if (!student) throw "Student not Found!";

    course.students = course.students.filter(s => s.userID !== studentID);
    student.courses = student.courses.filter(c => c.courseID !== courseID);

    return course;
  }
}

class Assingments {
  constructor(courses) {
    this.courses = courses;
    this.assingmentID = 0;
    this.assingments = [];
    this.assingmentGradesID = 0;
    this.AssingmentGrades = [];
  }

  getAssingments() {
    return this.assingments;
  }

  getAssingment(assingmentID) {
    return this.assingments.filter(a => a.assingmentID === assingmentID);
  }

  createAssingment(courseID, name) {
    const course = this.courses.getCourse(courseID);

    if (!course) throw "Course not Found";

    assingment_new = { assignmentID: this.assingmentID, name: name };
    this.assingmentID++;

    if (!course.assingments) {
      course.assigments = [assingment_new];
    } else if (course.asignments.name !== name) {
      this.assingments.push(assingment_new);
      course.assigments.push(assingment_new);
    }
    return assingment_new;
  }

  deleteAssingment(assingmentID) {
    const assingment = this.getAssingment(assingmentID);

    if (!assingment) throw "Assingment not Found";

    this.assingments = this.assingments.filter(
      a => a.assingmentID !== assingmentID
    );
    this.courses.assingments = this.courses.assingments.filter(
      a => a.assingmentID !== assingmentID
    );

    return assingment;
  }

  createAssingmentGrade(assingmentID, studentID, grade) {
    const assingment = this.getAssingment(assingmentID);
    const student = this.courses.students.filter(
      s => s.studentID === studentID
    );

    if (!assingment) throw "Assingment not Found";
    if (!student) throw "Student not Found";

    assingmentGrade = {
      assingmentGradesID: this.assingmentGradesID,
      assingmentID: assingmentID,
      studentID: studentID,
      grade: grade
    };

    this.AssingmentGrades.filpushter(assingmentGrade);
    this.assingmentGradesID++;

    return assingmentGrade;
  }
}

const users = new Users();
const courses = new Courses(users);
const assingments = new Assingments(courses);

// Provide resolver functions for your schema fields
const resolvers = {
  Query: {
    hello: (root, args, context) => `Hello ${args.name}!`,

    users: (root, args, context) => users.getUsers(),
    students: (root, args, context) => users.filterUsers("Student"),
    faculties: (root, args, context) => users.filterUsers("Faculty"),

    student: (root, args, context) =>
      users.filterUser(args.email, args.userID, "Student"),
    faculty: (root, args, context) =>
      users.filterUser(args.email, args.userID, "Faculty"),

    courses: (root, args, context) => courses.getCourses()
  },

  Mutation: {
    createUser: (root, args, context) =>
      users.createUser(args.name, args.email, args.role),

    createCourse: (root, args, context) =>
      courses.createCourse(args.name, args.facultyID),
    deleteCourse: (root, args, context) => courses.deleteCourse(args.courseID),
    addCourseStudent: (root, args, context) =>
      courses.addCourseStudent(args.courseID, args.studentID),
    deleteCourseStudent: (root, args, context) =>
      courses.deleteCourseStudent(args.courseID, args.studentID),

    createAssignment: (root, args, context) =>
      assingments.createAssignment(args.courseID, args.name),
    deleteAssignment: (root, args, context) =>
      assingments.deleteAssignment(args.assignmentID),
    deleteCourseStudent: (root, args, context) =>
      assingments.deleteCourseStudent(
        args.assignmentID,
        args.studentID,
        args.grade
      )
  },

  User: {
    __resolveType: (user, context, info) => user.role
  }
};

const server = new ApolloServer({
  typeDefs,
  resolvers
});

server.listen().then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});
