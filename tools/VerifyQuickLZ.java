import java.nio.file.*;
import java.io.*;
import java.util.*;
import com.thatguys.utils.QuickLZ;
class VerifyQuickLZ {
 public static void main(String[] args) throws Exception {
  byte[] data=Files.readAllBytes(Path.of(args[0]));
  byte[] expected=Files.readAllBytes(Path.of(args[1]));
  ByteArrayOutputStream out=new ByteArrayOutputStream();
  out.write(data,0,40);
  int offset=40,blocks=0;
  while(data.length-offset>=4096 || ((data[offset]&255)==79 || (data[offset]&255)==78)) {
   if ((data[offset]&255)!=79 && (data[offset]&255)!=78) break;
   byte[] remaining=Arrays.copyOfRange(data,offset,data.length);
   int size=(int)QuickLZ.sizeCompressed(remaining);
   int decoded=(int)QuickLZ.sizeDecompressed(remaining);
   if(decoded!=4096)throw new IllegalStateException("Decoded block size is not 4096: "+decoded);
   byte[] block=QuickLZ.decompress(Arrays.copyOfRange(data,offset,offset+size));
   out.write(block);
   offset+=size;blocks++;
   if(offset==data.length)break;
  }
  out.write(data,offset,data.length-offset);
  if(!Arrays.equals(expected,out.toByteArray()))throw new IllegalStateException("QuickLZ output differs from expected raw file");
  System.out.println("QuickLZ reference PASS: "+blocks+" blocks, "+(data.length-offset)+" raw tail bytes, full output identical");
 }
}
