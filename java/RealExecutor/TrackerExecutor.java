import smx.tracker.MeasurePointData;
import MMT.tracker.Tracker;

public class TrackerExecutor implements CommandExecutor {
    private Tracker tracker;
    public TrackerExecutor(Tracker tracker) {
	this.tracker = tracker;
    }

    public String execute(String[] command) throws Exception {
	double r, theta, phi;
	switch (command[0]) {
	case "connect":
	    this.tracker.connect();
	    return "";
	case "disconnect":
	    this.tracker.disconnect();
	    return "";
	case "move":
	case "move absolute":
	    r = new Double(command[1]);
	    theta = new Double(command[2]);
	    phi = new Double(command[3]);
	    if (command[0].equals("move"))
		this.tracker.move(r, theta, phi);
	    else
		this.tracker.move_absolute(r, theta, phi);
	    return "";
	case "search":
	    r = new Double(command[1]);
	    this.tracker.search(r);
	    return "";
	case "measure":
	    MeasurePointData m = this.tracker.measure(1)[0];
	    return Double.toString(m.distance())
		+" "+Double.toString(m.zenith())
		+" "+Double.toString(m.azimuth());
	case "abort":
	    this.tracker.abort();
	    return "";
	default:
	    throw new RuntimeException(PipeInterface.UNRECOGNIZED);
        }
    }
}