import org.opencv.core.Point;
import java.util.*;

public class GridSolver {

    public static List<Point> bfs(char[][] grid, Point start, Point end) {
        int rows = grid.length;
        int cols = grid[0].length;
        boolean[][] visited = new boolean[rows][cols];
        Point[][] parent = new Point[rows][cols];

        Queue<Point> queue = new LinkedList<>();
        queue.add(start);
        visited[(int)start.y][(int)start.x] = true;

        int[] dx = {1, -1, 0, 0};
        int[] dy = {0, 0, 1, -1};

        while (!queue.isEmpty()) {
            Point curr = queue.poll();
            if (curr.equals(end)) break;

            for (int i = 0; i < 4; i++) {
                int nx = (int)curr.x + dx[i];
                int ny = (int)curr.y + dy[i];

                if (nx >= 0 && ny >= 0 && nx < cols && ny < rows &&
                    grid[ny][nx] == ' ' && !visited[ny][nx]) {
                    queue.add(new Point(nx, ny));
                    visited[ny][nx] = true;
                    parent[ny][nx] = curr;
                }
            }
        }

        List<Point> path = new ArrayList<>();
        Point p = end;
        while (p != null && parent[(int)p.y][(int)p.x] != null) {
            path.add(0, p);
            p = parent[(int)p.y][(int)p.x];
        }
        if (!path.isEmpty()) path.add(0, start);

        return path;
    }
}
