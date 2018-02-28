import unittest

from .. import parse, parser, tree


POSITION_FOR1 = """public class Lambda {

    public static void main(String args[]) {
        for (int i = 0; i < 10; i++) {
        }
    }
}
"""

POSITION_FOR2 = """public class Lambda {

    public static void main(String args[]) {
        int i = 0;
        for (; i < 10; i++) {
        }
    }
}
"""

POSITION_FOR3 = """public class Lambda {

    public static void main(String args[]) {
        String[] str = {"1", "2", "3"};
        for (String s : str) {
        }
    }
}
"""

POSITION_METHOD = """public class Lambda {

    public String[] main(String args[]) {
        try {

        } catch(Exception e) {

        }

        if (true) {

        }
        return args;
    }
}
"""

POSITION_TRY_CATCH = """public class Lambda {

    public static void main(String args[]) {
        try {

        } catch(Exception e) {

        }

        if (true) {

        }
    }

    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        EditText inputText = (EditText) findViewById(R.id.input_entry);
        inputText.setText(
                desc,
                android.widget.TextView.BufferType.EDITABLE
        );

//
        Button encryptIntentButton = (Button) findViewById(R.id.encrypti);
        Button decryptIntentButton = (Button) findViewById(R.id.decrypti);
        Button getButton = (Button) findViewById(R.id.get);
        Button setButton = (Button) findViewById(R.id.set);
        Button outToInButton = (Button) findViewById(R.id.outToIn);
        Button spoofme = (Button) findViewById(R.id.spoof_me);

        encryptIntentButton.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View arg0) {
                        clickMaster(ENCRYPT_REQUEST);
                    }
                }
        );
        decryptIntentButton.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View arg0) {
                        clickMaster(DECRYPT_REQUEST);
                    }
                }
        );
        getButton.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View arg0) {
                        clickMaster(GET_PASSWORD_REQUEST);
                    }
                }
        );
        setButton.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View arg0) {
                        clickMaster(SET_PASSWORD_REQUEST);
                    }
                }
        );
//
        outToInButton.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View arg0) {
                        EditText outputText = (EditText) findViewById(R.id.output_entry);
                        EditText inputText = (EditText) findViewById(R.id.input_entry);
                        String newInputStr = outputText.getText().toString();
                        inputText.setText(newInputStr, android.widget.TextView.BufferType.EDITABLE);

                    }
                }
        );
        spoofme.setOnClickListener(
                new View.OnClickListener() {
                    public void onClick(View arg0) {
                        Intent i = new Intent();
                        i.setAction(Intent.ACTION_MAIN);
                        i.setClassName("org.openintents.safe", "org.openintents.safe.AskPassword");
                        startActivityForResult(i, SPOOF_REQUEST);
                    }
                }
        );

    }//oncreate
    // hallo welt
}
"""


class TestPositions(unittest.TestCase):

    def test_for1(self):
        ast = parse.parse(POSITION_FOR1)
        for path, node in ast.filter(tree.ForStatement):
            self.assertEqual(len(node.position), 2)
            self.assertEqual(node.position[0], 4)
            self.assertEqual(node.position[1], 9)

        for path, node in ast.filter(tree.ForControl):
            self.assertEqual(len(node.position), 2)
            self.assertEqual(node.position[0], 4)
            self.assertEqual(node.position[1], 14)

    def test_for2(self):
        ast = parse.parse(POSITION_FOR2)
        for path, node in ast.filter(tree.ForControl):
            self.assertEqual(len(node.position), 2)
            self.assertEqual(node.position[0], 5)
            self.assertEqual(node.position[1], 14)

    def test_enhanced_for(self):
        ast = parse.parse(POSITION_FOR3)
        for path, node in ast.filter(tree.ForStatement):
            self.assertEqual(len(node.position), 2)
            self.assertEqual(node.position[0], 5)
            self.assertEqual(node.position[1], 9)

        for path, node in ast.filter(tree.EnhancedForControl):
            self.assertEqual(len(node.position), 2)
            self.assertEqual(node.position[0], 5)
            self.assertEqual(node.position[1], 14)

    def test_try_catch(self):
        ast = parse.parse(POSITION_TRY_CATCH)
        for path, node in ast.filter(tree.TryStatement):
            self.assertEqual(len(node.position), 2)
            self.assertEqual(node.position[0], 4)
            self.assertEqual(node.position[1], 9)

        for path, node in ast.filter(tree.CatchClause):
            self.assertEqual(len(node.position), 2)
            self.assertEqual(node.position[0], 6)
            self.assertEqual(node.position[1], 11)

        for path, node in ast.filter(tree.MethodDeclaration):
            if node.name == 'main':
                self.assertEqual(node.position[0], 3)
                self.assertEqual(node.position[1], 19)

                self.assertEqual(node.end_position[0], 13)
                self.assertEqual(node.end_position[1], 5)
            if node.name == 'onCreate':
                self.assertEqual(node.position[0], 15)
                self.assertEqual(node.position[1], 12)

                self.assertEqual(node.end_position[0], 84)
                self.assertEqual(node.end_position[1], 5)

    def test_method_non_void(self):
        ast = parse.parse(POSITION_METHOD)
        for path, node in ast.filter(tree.MethodDeclaration):
            if node.name == 'main':
                self.assertEqual(node.position[0], 3)
                self.assertEqual(node.position[1], 12)

                self.assertEqual(node.end_position[0], 14)
                self.assertEqual(node.end_position[1], 5)

if __name__ == "__main__":
    unittest.main()
