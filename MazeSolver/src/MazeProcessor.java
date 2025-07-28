import org.opencv.core.*;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;

public class MazeProcessor {

    public static Mat loadAndBinarize(String path) {
        Mat src = Imgcodecs.imread(path, Imgcodecs.IMREAD_GRAYSCALE);
        if (src.empty()) throw new IllegalArgumentException("Errore caricamento immagine: " + path);

        Mat binary = new Mat();
        Imgproc.threshold(src, binary, 100, 255, Imgproc.THRESH_BINARY); // sensibile ai muri neri
        return binary;
    }

    public static Point findRedPixel(Mat colorImage) {
        for (int y = 0; y < colorImage.rows(); y++) {
            for (int x = 0; x < colorImage.cols(); x++) {
                double[] pixel = colorImage.get(y, x);
                if (pixel != null && pixel[2] > 200 && pixel[1] < 50 && pixel[0] < 50) {
                    return new Point(x, y);
                }
            }
        }
        return null;
    }

    public static Point findRedPixelOnBorder(Mat colorImage) {
        int rows = colorImage.rows();
        int cols = colorImage.cols();

        for (int x = 0; x < cols; x++) {
            double[] pixel = colorImage.get(0, x);
            if (isRed(pixel)) return new Point(x, 0);
            pixel = colorImage.get(rows - 1, x);
            if (isRed(pixel)) return new Point(x, rows - 1);
        }

        for (int y = 0; y < rows; y++) {
            double[] pixel = colorImage.get(y, 0);
            if (isRed(pixel)) return new Point(0, y);
            pixel = colorImage.get(y, cols - 1);
            if (isRed(pixel)) return new Point(cols - 1, y);
        }

        return null;
    }

    private static boolean isRed(double[] pixel) {
        return pixel != null && pixel[2] > 200 && pixel[1] < 50 && pixel[0] < 50;
    }
}
