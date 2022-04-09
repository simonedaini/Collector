import xlsxwriter

# Create an new Excel file and add a worksheet.
workbook = xlsxwriter.Workbook('images.xlsx')
worksheet = workbook.add_worksheet("Evidence-Timeline")

# Widen the first column to make the text clearer.
worksheet.set_column('A:A', 30)

# Insert an image with scaling.
worksheet.write('A1', 'Insert a scaled image:')
worksheet.insert_image('B1', 'test.png', {
    'x_offset':    25,
    'y_offset':    25,
    'x_scale':     0.5,
    'y_scale':     0.5,
    'url':         None,
    'tip':         None,
    'image_data':  None,
    'positioning': None,
})

workbook.close()