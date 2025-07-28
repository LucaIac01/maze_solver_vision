import org.opencv.core.*;
import org.opencv.imgcodecs.Imgcodecs;
import java.util.List;

public class Main {
    static { System.loadLibrary(Core.NATIVE_LIBRARY_NAME); }

    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("Uso: java Main <input_image>");
            return;
        }

        String inputPath = args[0];
        String outputPath = "../output/solved_maze.png";

        // 1. Carica immagini
        Mat binary = MazeProcessor.loadAndBinarize(inputPath);
        Mat color = Imgcodecs.imread(inputPath);

        // 2. Trova pixel rossi
        Point start = MazeProcessor.findRedPixel(color);
        Point end = MazeProcessor.findRedPixelOnBorder(color);

        if (start == null || end == null) {
            System.out.println("❌ Start o Exit non trovati.");
            return;
        }

        char[][] grid = GridExtractor.extractGrid(binary);

        // 3. Debug: verifica tipo di cella
        System.out.println("🧪 Valore start: '" + grid[(int)start.y][(int)start.x] + "'");
        System.out.println("🧪 Valore exit:  '" + grid[(int)end.y][(int)end.x] + "'");

        // 4. Correggi se servono
        start = nearestOpenPixel(grid, start);
        end = nearestOpenPixel(grid, end);

        System.out.println("🚩 Start: " + start);
        System.out.println("🏁 Exit:  " + end);

        // 5. Calcola percorso
        List<Point> path = GridSolver.bfs(grid, start, end);

        if (path.isEmpty()) {
            System.out.println("❌ Nessun percorso trovato!");
        } else {
            System.out.println("✅ Percorso trovato! Lunghezza: " + path.size());
            MazeDrawer.drawPath(inputPath, outputPath, path);
        }
    }

    // 🔧 Cerca il primo punto camminabile vicino a quello indicato
    public static Point nearestOpenPixel(char[][] grid, Point origin) {
        int rows = grid.length;
        int cols = grid[0].length;

        int[] dx = {1, -1, 0, 0};
        int[] dy = {0, 0, 1, -1};

        boolean[][] visited = new boolean[rows][cols];
        java.util.Queue<Point> q = new java.util.LinkedList<>();

        int ox = (int) origin.x;
        int oy = (int) origin.y;

        q.add(new Point(ox, oy));
        visited[oy][ox] = true;

        while (!q.isEmpty()) {
            Point p = q.poll();
            int x = (int) p.x, y = (int) p.y;

            if (grid[y][x] == ' ') return new Point(x, y);

            for (int i = 0; i < 4; i++) {
                int nx = x + dx[i];
                int ny = y + dy[i];

                if (nx >= 0 && ny >= 0 && nx < cols && ny < rows && !visited[ny][nx]) {
                    visited[ny][nx] = true;
                    q.add(new Point(nx, ny));
                }
            }
        }

        return origin; // fallback
    }
}
