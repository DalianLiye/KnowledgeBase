```Java
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

public class test {
    public static void main(String[] args) throws Exception {
        //创建一个字符流，从标准输入中读取数据
        ANTLRInputStream input = new ANTLRInputStream(System.in);

        //新建一个词法分析器，处理输入的字符流
        XXXXXLexer lexer = new XXXXXLexer(input);

        //新建一个词法符号的缓冲区,用于存储词法分析器将生成的词法符号
        CommonTokenStream tokens = new CommonTokenStream(lexer);

        //新建一个语法分析器,处理词法符号缓冲区中的内容
        XXXXXParser parser = new XXXXXParser(tokens);

        //针对语法文件中的语法规则xxxx,开始语法分析
        ParseTree tree =  parser.xxxx();

        //新建一个通用的，能够触发回调函数的语法分析树遍历器
        ParseTreeWalker walker = new ParseTreeWalker();

        //遍历语法分析过程中生成的语法分析树，触发回调
        //new XXXXXXX()是继承了XXXXXBaseListener类，并实现了指定语法规则函数(enter或exit方法)的类的对象
        //可以根据需求的不同，而传递不同的实例，比如YYYYYY()继承了XXXXXBaseListener类，并实现了其他语法规则函数，那么就将new YYYYYY()作为第一个参数传递进去
        walker.walk(new XXXXXXX(),tree);

        //用LISP风格打印生成的树
        System.out.println(tree.toStringTree(parser));
    }
}


```