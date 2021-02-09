import datetime
import xlsxwriter

class ExportExcel:
    directory = "."

    @staticmethod
    def createXlsx(data):
        def ntc(i):
            if i < 26:
                return str(chr(65+i))
            else:
                return ntc(int(i/26)-1)+ntc(i % 26)
        filePath = 'result_'+datetime.datetime.now().strftime("%x%X%f").replace('/', '_').replace(':', '_')+'.xlsx'
        # print "=== path xlsx ==="
        # print ExportExcel.directory+filePath
        # print "============"
        workbook = xlsxwriter.Workbook(ExportExcel.directory+'/'+filePath)
        worksheet = workbook.add_worksheet()
        format_0 = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter'
        })
        format_0.set_bold()
        format_0.set_border()
        format_1 = workbook.add_format({
            'align': 'left',
            'valign': 'top'
        })
        format_1.set_border()
        format_2 = workbook.add_format({
            'align': 'left',
            'valign': 'vtop'
        })
        format_2.set_text_wrap()
        format_2.set_border()
        
        row = 0
        col_1 = ['ticker', 'year']
        
        # print header
        col_num = 0
        for col_name in col_1:
            worksheet.merge_range(ntc(col_num)+str(row+1)+':'+ntc(col_num)+str(row + 2), col_name, format_0)
            col_num += 1
        if len(data) <= 0:
            return None
        if len(data[0]['num_of_words']) > 1:
            worksheet.merge_range(ntc(col_num)+str(row+1)+':'+ntc(col_num+len(data[0]['num_of_words']) - 1)+str(row + 1), "kata", format_0)
        else:
            worksheet.write(row, col_num, "kata", format_0)
        col_num = len(col_1)
        row += 1
        for n in data[0]['num_of_words']:
            worksheet.write(row, col_num, n['word'], format_0)
            col_num += 1
        row += 1
        # prin data menurun only negativetone
        max_kal = 0
        
        for r in data:
            col_num = 0
            if len(r['sentences']) > max_kal:
                max_kal = len(r['sentences'])
            for col_name in col_1:
                worksheet.write(row, col_num, r[col_name], format_1)
                col_num += 1
            for n in r['num_of_words']:
                worksheet.write(row, col_num, n['total'], format_1)
                col_num += 1
            neg_tone = {}
            for sentence in r['sentences']:
                if 'negative tone' in sentence:
                    for kata in sentence['negative tone'].keys():
                        if kata not in neg_tone:
                            neg_tone[kata] = 0
                        neg_tone[kata] += sentence['negative tone'][kata]
            if 'negative tone' in data[0]["sentences"][0]:
                for kata in data[0]["sentences"][0]['negative tone'].keys():
                    if kata in neg_tone:
                        worksheet.write(row, col_num, neg_tone[kata], format_1)
                    else:
                        worksheet.write(row, col_num, 0, format_1)
                    col_num += 1
            row += 1  
        col_num = len(col_1) + len(data[0]['num_of_words'])

        if len(data) > 0 and 'negative tone' in data[0]["sentences"][0]:
            worksheet.merge_range(ntc(col_num)+str(1)+':'+ntc(col_num+len(data[0]["sentences"][0]['negative tone']) - 1)+str(1), "negative tone", format_0)
            for kata in data[0]["sentences"][0]['negative tone'].keys():
                worksheet.write(1, col_num, kata, format_0)
                col_num += 1
        
        try:
            workbook.close()
        except Exception as e:
            print(e)
        return filePath
    