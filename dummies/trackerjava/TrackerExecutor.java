public class TrackerExecutor implements CommandExecutor {
    public TrackerExecutor() {}
    public String execute(String[] command) throws Exception {
	double r, theta, phi;
	String cmdword = command[0];
	if (cmdword.equals("connect") || cmdword.equals("disconnect") ||
	    cmdword.equals("move") || cmdword.equals("move absolute") ||
	    cmdword.equals("search") || cmdword.equals("abort") ||
	    cmdword.equals("set mode"))
	    return "";
	else if (cmdword.equals("measure"))
	    return "0 0 0";
	else
	    throw new RuntimeException(PipeInterface.UNRECOGNIZED);
    }
}