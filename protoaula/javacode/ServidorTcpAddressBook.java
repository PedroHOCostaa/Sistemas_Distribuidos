import java.io.DataInputStream;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

public class ServidorTcpAddressBook {
    public static void main(String args[]) {
        try {
            int serverPort = 7000;
            ServerSocket listenSocket = new ServerSocket(serverPort);
            while (true) {
                Socket clientSocket = listenSocket.accept();

                DataInputStream inClient = 
                    new DataInputStream(clientSocket.getInputStream());
                
                String valueStr = inClient.readLine();
                int sizeBuffer = Integer.valueOf(valueStr);
                byte[] buffer = new byte[sizeBuffer];
                inClient.read(buffer);

                Addressbook.Person p = Addressbook.Person.parseFrom(buffer);

                System.out.println("---\n" + p + "---\n");
            }
        } catch (IOException e) {
            System.out.println("Listen Socket: " + e.getMessage());
        }
    }
}
