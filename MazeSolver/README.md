# 🧠 Maze Solver Vision (Java + OpenCV)

This project implements a **maze solver** in Java using OpenCV. It analyzes an input maze image and finds the **shortest path** from a start point to an exit, then draws the path **centered through the corridors**.

---

## 📷 Input Format

* The **maze** is a grayscale PNG image.
* The **start point** is a solid **red square**.
* The **exit** is a thin **red line** on one of the image borders.

---

## ✅ Requirements

* Java 8 or higher
* OpenCV 4.13 (Java bindings)
* OS: Linux / macOS / Windows

---

## ⚙️ Setup

### 1. Clone the repository

```
git clone https://github.com/<your-username>/maze-solver-vision.git
cd maze-solver-vision/MazeSolver
```

### 2. OpenCV setup

Ensure you have the following files inside the `lib/` folder:

* `opencv-4130.jar`
* `libopencv_java4130.so` (for Linux) or `.dll` (for Windows)

If needed, build OpenCV from source with Java support.

---

### 3. Compile the project

```
cd src
javac -cp .:../lib/opencv-4130.jar *.java
```

> On Windows, replace `:` with `;` in the classpath.

---

## ▶️ Run the program

```
java -cp .:../lib/opencv-4130.jar -Djava.library.path=../lib Main ../images/input_maze.png
```

### Output:

* The solved maze image will be saved as: `output/solved_maze.png`

---

## 🧱 Project Structure

```
MazeSolver/
├── src/
│   ├── Main.java
│   ├── MazeProcessor.java
│   ├── MazeDrawer.java
│   ├── GridSolver.java
│   └── GridExtractor.java
├── lib/
│   └── opencv-4130.jar + .so/.dll
├── images/
│   └── input_maze.png
├── output/
│   └── solved_maze.png
```

---

## 🏁 Features

* ✅ Reads a maze from an image
* ✅ Automatically detects start and exit
* ✅ Finds the shortest path using BFS
* ✅ Draws the solution path **centered** inside corridors
* ✅ Designed for 15x20 cell mazes with thin 1-pixel walls

---

## 📄 License

MIT – Free to use for educational and personal purposes.
