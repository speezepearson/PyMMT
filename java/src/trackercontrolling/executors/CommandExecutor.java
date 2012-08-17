package trackercontrolling.executors;

public interface CommandExecutor {
    public String execute(String[] command) throws Exception;
}