from LexicalAnalyser import LexicalAnalyser

if __name__ == '__main__':
    # for file in ['p1.Z', 'p2.Z', 'p3.Z', 'p1err.Z']:
    #     lexical_analyser = LexicalAnalyser()
    #     lexical_analyser.parse(file)
    #     print(lexical_analyser)
    #     print('\n' + '=' * 30)

    filename = 'p1err.Z'
    lexical_analyser = LexicalAnalyser()
    lexical_analyser.parse(filename)
    lexical_analyser.output_files(filename)
