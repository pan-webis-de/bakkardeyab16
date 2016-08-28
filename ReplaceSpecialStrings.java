
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.Writer;
import java.util.regex.Matcher;
import java.util.regex.Pattern;







public class ReplaceSpecialStrings {

    String[] feelings = new String[266];

    public static void main(String args[]) throws Exception {
        // read the file (all the characters between §i to §f at once) as we have tweets with more than one line 

        ReplaceSpecialStrings rss = new ReplaceSpecialStrings();

        //rss.readFeelingList();

        File folder = new File("compiled_dataset");
        File[] listOfFiles = folder.listFiles();

        for (int i = 0; i < listOfFiles.length; i++) {
            rss.replacespecialsInOneFile(listOfFiles[i]);
        }

        //rss.replacespecialsInOneFile(listOfFiles[0]);
        //rss.test();
    }

    public void replacespecialsInOneFile(File file) throws Exception {

        System.out.println(file.getName());

        //int k = 0;//number of matches 
        String[] exp = {"http([^\\s§]+)", //   LINK_TAG
            "[:;]-[()]|:-[DO|\\\\\\/S*p]|;-[Dp]|:'-[D()]", // NOSY_EMOJI_TAG
            ":[']*[)(pO3D\\\\s|*\\]]*|:\\/|;[()Dp]|\\(:|[']*8\\)|x[dD][dD]*", // SIMPLE_EMOJI_TAG
            "<3|<joke\\/>|\\(K\\)", // FIGURE_EMOJI_TAG
            "=[()DP]", // FUNNY_EYES_EMOJI_TAG
            // HORIZ_EMOJI_TAG
            "-\\.-|\\*\\.\\*|\\^[\\.\\_\\-]\\^|\\^\\^|[\\\\]*\\(\\^o\\^\\)[\\/]*|o\\.O|[<>]\\.[<>]|u\\.u",
            // RUDE_TALK_TAG
            "[fF]\\*\\*\\*|([mM]other)*([mM]utha)*[fF]uck(er)*(ed)*(ing)*|[sS]tupid|[bB]oobs|[sS]hit(ty)*|[aA]sshole|[bB]itch| [aA]ss|[dD]icks",
            "what the fuck|WHAT THE FUCK|FUCK", //  RUDE_TALK_TAG
            //  LAUGH_TAG
            "haha(ha)*(h)*|HAHA(HA)*(H)*|ahah(ah)*(a)*|eheh(eh)*(e)*|ihih(ih)*(i)*|Lol|(rof)*l(o)+l|jaja(ja)*(a)*|(rotf)*lmao|lmfao|rotfl|([aA]*[jJ]+[aA]+)+",
            //  PUNCTUATION_ABUSE_TAG
            "!!(!)*|\\?\\?(\\?)*|\\.\\.\\.\\.(\\.)*|,,(,)*|(\\?+!+)+",
            // EXPRESSIONS_TAG
            " ugh(h)* |ouch(h)*|omg|whoa|[wW]oah|boo yah|hurray|hurrah|huh|(u)*uhhh(h)*|[wW]tf|(o)*ops(s)*|ohh(h)*|jk|aww(w)*|idk|WOW|wow|damn|DAMN|hm(m)*| oh |(o)+oh",
            // SHARE_PIC_TAG
            "\\[pic\\]",
            //  MENTION_TAG
            "@username",
            // HASHTAG_TAG
            "#([^\\s§]+)",
            // NEW_LINE_TAG
            "\n"};

        String[] aliases = {" _LINK_TAG ", //1
            " _NOSY_EMOJI_TAG ", //2
            " _SIMPLE_EMOJI_TAG ", //3
            " _FIGURE_EMOJI_TAG ", //4
            " _FUNNY_EYES_EMOJI_TAG ", //5
            " _HORIZ_EMOJI_TAG ", //6
            " _RUDE_TALK_TAG ", //7
            " _RUDE_TALK_TAG ", //8                  
            " _LAUGH_TAG ", //9
            " _PUNCTUATION_ABUSE_TAG ", //10
            " _EXPRESSIONS_TAG ", //11
            " _SHARE_PIC_TAG ", //12
            " _MENTION_TAG ", //13
            " _HASHTAG_TAG ",
            " _NEW_LINE_TAG "};            //14

        new File("tagged_dataset").mkdirs();


        PrintWriter writer = new PrintWriter("tagged_dataset/" + file.getName(), "UTF-8");

        FileInputStream fis = new FileInputStream(file);
        byte[] data = new byte[(int) file.length()];
        fis.read(data);
        fis.close();

        String str = new String(data, "UTF-8");

        //String y[] = str.split("[\\ufffd]f");
        String y[] = str.split("§f");

        String output = "";

        Pattern p;
        Matcher m;

        for (int i = 0; i < y.length - 1; i++) {
            String tweet = y[i];
            tweet = tweet.trim();
            tweet = tweet.substring(2, tweet.length());
            //System.out.println(tweet);            
            for (int j = 0; j < exp.length; j++) {

                // just to check which files have matches so we can verify the result manually.
                /*
                p = Pattern.compile(exp[j]);
                m = p.matcher(tweet);
                if (m.find()) {
                    System.out.println("match");

                }*/
                tweet = tweet.replaceAll(exp[j], aliases[j]);

               // tweet = tagFeeling(tweet);

            }

            tweet = "§i" + tweet + "§f\n";
            output += tweet;
            //output += "§f\n";
        }
        // output the final result 
        writer.println(output);
        writer.close();

        //System.out.println("number of matches:" + k);
        System.out.println("================");
    }

    public String tagFeeling(String tweet) {
        // Here we tag all the feelings in the tweet with the tag _FEELING_TAG

        for (int i = 0; i < feelings.length; i++) {

            tweet = tweet.replaceAll(feelings[i].trim(), " _FEELING_TAG ");
            //System.out.println("------------------------");

        }

        return tweet;
    }

    public void readFeelingList() throws Exception {

        int i = 0;

        BufferedReader br = new BufferedReader(new FileReader("feelings.txt"));
        String line = br.readLine();
        while (line != null) {
            feelings[i] = line.trim();
            i++;
            line = br.readLine();
        }

        
    }

    public void test() throws Exception {
        /*
        String str = ":-) is out new tag";
        str = str.replaceAll("[:;]-[()]|:-[DO|\\\\\\/S*p]|;-[Dp]|:'-[D()]", "nosy_emoji_tag");
        System.out.println(str);
        
         

        String g = "§i@username that tweet was mainly for you ;-) cheers!§f\n"
                + "§iI am watching Person of Interest, Pilot (S01E01). http://t.co/Hp9AgJG1§f";

        String t[] = g.split("§f");

        System.out.println(t[0]);*/

        String str = "sdfsdf \n sdfsdf";
        str = str.replaceAll("\n", "newlinetag");
        System.out.println(str);

    }

}
