import random
import string
import re
from pygments import highlight
from pygments.lexers import guess_lexer, get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

class Coding:
    def __init__(self):
        self.containsACode = False
        self.in_coding = False
        self.activation = False
        self.deactivation = False
        self.ID = None
        self.language = None
        self.lexer = None
        self.code_lines = None  # lines of code upon conversion
        self.code_str = None    # lines of code from verbatim
        
    def reset(self):
        self.ID = None
        self.language = None
        self.lexer = None
        self.code_lines = None
        self.code_str = None
        

    def resetActivation(self):
        self.activation = False
        self.deactivation = False

    def activate(self):
        self.in_coding = True
        self.activation = True
        self.containsACode = True

    def randomGen(self, id_prefix="code"):
        # one-shot ID
        random_id = ''.join(random.choices(string.digits, k=16))
        self.ID = f"{id_prefix}-{random_id}"
        
    def guessLanguage(self):

        try:
            self.lexer = guess_lexer(self.code_str)
            self.language = self.lexer.aliases[0] if self.lexer.aliases else "text"

        except ClassNotFound:
                self.language = "text"
                self.lexer = get_lexer_by_name("text")

    def codeText(self):
        formatter = HtmlFormatter(nowrap=True)
        highlighted_code = highlight(self.code_str, self.lexer, formatter)
        self.code_lines = highlighted_code.strip().split('\n')


    def convert(self):

        # prepare
        self.randomGen()
        self.guessLanguage()
        self.codeText()
        
        # Construct numbered lines
        gutter_lines = ""
        code_content_lines = ""
        for i, line in enumerate(self.code_lines, start=1):
            gutter_lines += f'<span class="line">{i}</span><br>'
            code_content_lines += f'<span class="line">{line}</span><br>'
        
        # Final assembly
        html_block = f"""
            <figure class="highlight {self.language} hljs" id="{self.ID}">
              <figcaption class="level is-mobile">
                <div class="level-left">
                  <span class="fold">
                    <i class="fas fa-angle-down"></i>
                  </span>
                </div>
                <div class="level-right">
                  <a href="javascript:;" class="copy" title="Copy" data-clipboard-target="#{self.ID} .code">
                    <i class="fas fa-copy"></i>
                  </a>
                </div>
              </figcaption>
              <div class="highlight-body">
                <table>
                  <tbody>
                    <tr>
                      <td class="gutter">
                        <pre>{gutter_lines}</pre>
                      </td>
                      <td class="code">
                        <pre>{code_content_lines}</pre>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </figure>
            """
        return html_block


    def write(self, file, stripped_line):
        if not self.activation:
            if not self.deactivation:
                if self.code_str == None:
                    self.code_str = stripped_line
                else:
                    self.code_str = self.code_str + stripped_line
            else:
                html_block = self.convert()
                file.write(html_block)
                self.in_coding = False
                self.reset()


    def createScript(self,file):

        code_block = """
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.5.1/styles/atom-one-light.min.css">

        <script>
        // Selecting all copy buttons
        document.querySelectorAll('.copy').forEach(button => {
            button.addEventListener('click', function() {
                // Find the element with the correct ID for following copy
                const codeElement = document.querySelector(this.getAttribute('data-clipboard-target'));
                const range = document.createRange();
                range.selectNode(codeElement);
                window.getSelection().removeAllRanges();
                window.getSelection().addRange(range);
                
                try {
                    // Copy selected text
                    document.execCommand('copy');
                    // Change the icon to point out the copy has been completed
                    const icon = this.querySelector('i');
                    icon.classList.remove('fa-copy');
                    icon.classList.add('fa-check'); // ICON NOW CHECKMARKED
                    setTimeout(() => {
                        icon.classList.remove('fa-check');
                        icon.classList.add('fa-copy'); 
                    }, 2000);                       // AFTER 2s GO BACK TO STD COPY ICON
                } catch (err) {
                    console.error('Impossibile copiare il testo: ', err);
                }
                
                window.getSelection().removeAllRanges();
            });
        });

        // Selecting all fold/unfold buttons
        document.querySelectorAll('.fold').forEach(foldButton => {
            foldButton.addEventListener('click', function() {
                // Find block to fold/unfold based on ID
                const codeBlock = this.closest('figure').querySelector('.highlight-body');
                const icon = this.querySelector('i');

                // If visible -> make fold and change arrow
                // else -> do the opposite
                if (codeBlock.style.display !== 'none') {
                    codeBlock.style.display = 'none';
                    icon.classList.remove('fa-angle-down');
                    icon.classList.add('fa-angle-right'); // >
                } else {
                    codeBlock.style.display = 'block';
                    icon.classList.remove('fa-angle-right');
                    icon.classList.add('fa-angle-down'); // v
                }
            });
        });
        </script>
        """
        file.write(code_block)


