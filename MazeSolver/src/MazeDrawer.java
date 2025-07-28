import org.opencv.core.*;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;
import java.util.ArrayList;
import java.util.List;


public class MazeDrawer {
    public static void drawPath(String inputPath, String outputPath, List<Point> path) {
        Mat image = Imgcodecs.imread(inputPath, Imgcodecs.IMREAD_COLOR);

        Scalar pathColor = new Scalar(0, 255, 0);     // verde
        Scalar startColor = new Scalar(0, 255, 255);  // giallo
        Scalar endColor = new Scalar(0, 0, 255);      // rosso

        int mazeWidth = image.cols();
        int mazeHeight = image.rows();

        int cols = 20; // numero celle per riga
        int rows = 15; // numero celle per colonna

        int cellWidth = mazeWidth / cols;
        int cellHeight = mazeHeight / rows;

        // 🔄 Converte punti del path nei centri delle celle
        List<Point> centeredPath = new ArrayList<>();
        for (Point p : path) {
            int col = (int)(p.x / cellWidth);
            int row = (int)(p.y / cellHeight);
            int centerX = col * cellWidth + cellWidth / 2;
            int centerY = row * cellHeight + cellHeight / 2;
            centeredPath.add(new Point(centerX, centerY));
        }

        // 🟢 Traccia il percorso centrato
        for (int i = 1; i < centeredPath.size(); i++) {
            Point p1 = centeredPath.get(i - 1);
            Point p2 = centeredPath.get(i);
            Imgproc.line(image, p1, p2, pathColor, 2);
        }

        // 🔴 Start & End
        if (!centeredPath.isEmpty()) {
            Imgproc.circle(image, centeredPath.get(0), 4, startColor, -1);
            Imgproc.circle(image, centeredPath.get(centeredPath.size() - 1), 4, endColor, -1);
        }

        Imgcodecs.imwrite(outputPath, image);
        System.out.println("💾 Percorso salvato (centrato) in: " + outputPath);
    }
}

