import pypandoc

output = pypandoc.convert(source='D:\\Passion\\Machine Learning\\\Projects\\Semantic_Web_Parser_Model_Builder\\Second Model Preparation\demo.html', format='html', to='docx', outputfile='C:\\Users\\Swaroop Nath\\Desktop\\demo.docx', extra_args=['-RTS'])