import org.opencv.core.Mat;

public class GridExtractor {

    public static char[][] extractGrid(Mat binaryImage) {
        int rows = binaryImage.rows();
        int cols = binaryImage.cols();

        char[][] grid = new char[rows][cols];

        for (int y = 0; y < rows; y++) {
            for (int x = 0; x < cols; x++) {
                double[] pixel = binaryImage.get(y, x);
                grid[y][x] = (pixel != null && pixel[0] == 0) ? '#' : ' ';
            }
        }

        return grid;
    }

    public static void printGrid(char[][] grid) {
        for (char[] row : grid) {
            for (char c : row) System.out.print(c);
            System.out.println();
        }
    }
}
