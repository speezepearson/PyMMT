import java.io.IOException;

public class TrackerPipeMain {
    public static void main(String[] args) {
	CommandExecutor executor = new TrackerExecutor();
	while (true)
	    try {
		PipeInterface.readExecuteWrite(executor);
	    } catch (IOException e) {}
    }
}