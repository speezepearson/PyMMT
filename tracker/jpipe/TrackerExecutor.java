public class TrackerExecutor implements CommandExecutor {
    public String execute(String command) throws Exception {
        if (command.startsWith("sum ")) {
            String[] split = command.split(" ");
            double result = 0;
            for (int i=1; i<split.length; i++)
                result += new Double(split[i]);
            return Double.toString(result);
        }
        else {
	    throw new RuntimeException(PipeInterface.UNRECOGNIZED);
        }
    }
}