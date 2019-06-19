import pypandoc

output = pypandoc.convert(source='C:\\Users\\Swaroop Nath\\Desktop\\demo.html', format='html', to='docx', outputfile='C:\\Users\\Swaroop Nath\\Desktop\\demo.docx', extra_args=['-RTS'])