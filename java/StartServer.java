import py4j.GatewayServer;

public class StartServer {
    public static void main(String[] args) {
        GatewayServer gatewayServer = new GatewayServer(null);
        gatewayServer.start();
        System.out.println("Gateway Server Started");
    }

}