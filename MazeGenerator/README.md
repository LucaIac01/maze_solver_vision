# 🧱 Maze Generator (20×15)

This Python project generates a random maze of configurable size (e.g., 20 columns × 15 rows). The output is saved as a PNG image inside the `maze_image/` folder.

---

## 🧩 Features

- ✅ Generates random, solvable mazes  
- ✅ Image output saved with custom filename  
- ✅ Supports any maze size via arguments  
- ✅ Suitable for integration with pathfinding algorithms  

---

## 🐍 Requirements

- Python 3.7+  
- Pillow (Python Imaging Library)

Install it with:

pip install pillow


---

## ▶️ How to Run

From the project root, run the script with **3 arguments**:

python maze_gen.py <width> <height> <filename>


### Example:

python maze_gen.py 20 15 maze_20x15


This will generate a `20 × 15` maze and save the image to:

maze_image/maze_20x15.png


---

## 🧱 Maze Structure

- Black pixels: walls (1-pixel thick) 
- White pixels: corridors 
- No start/end markers (you can add them separately)

---

## 📁 Project Structure

MazeGenerator/
├── maze_gen.py
├── maze_image/
│ └── maze_20x15.png ← output example


---

## 📄 License

MIT – Free for educational and personal use.
