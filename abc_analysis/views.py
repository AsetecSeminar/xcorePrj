import pandas as pd
from django.shortcuts import render, redirect
from .forms import UploadFileForm
from .models import ProductMaster, Shipment

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # 엑셀 파일 읽기
            excel_file = request.FILES['file']
            df = pd.read_excel(excel_file)

            # 제품 마스터 정보 저장
            for _, row in df.iterrows():
                product, created = ProductMaster.objects.get_or_create(
                    product_code=row['product_code'],
                    defaults={
                        'product_name': row['product_name'],
                        'category': row['category'],
                        'price': row['price']
                    }
                )
                
                # 출고 정보 저장
                Shipment.objects.create(
                    product=product,
                    quantity=row['quantity'],
                    shipment_date=row['shipment_date']
                )
            
            return redirect('abc_analysis')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def abc_analysis(request):
    # 출고 금액 계산
    shipments = Shipment.objects.all()
    analysis_data = {}

    for shipment in shipments:
        product = shipment.product
        revenue = shipment.quantity * product.price

        if product.product_code not in analysis_data:
            analysis_data[product.product_code] = {
                'product_name': product.product_name,
                'total_revenue': 0,
                'category': product.category
            }
        
        analysis_data[product.product_code]['total_revenue'] += revenue

    # 총 출고 금액 계산
    total_revenue = sum(item['total_revenue'] for item in analysis_data.values())

    # ABC 분류
    sorted_data = sorted(analysis_data.items(), key=lambda x: x[1]['total_revenue'], reverse=True)
    cumulative_revenue = 0
    for idx, (product_code, data) in enumerate(sorted_data):
        cumulative_revenue += data['total_revenue']
        cumulative_percentage = cumulative_revenue / total_revenue * 100

        if cumulative_percentage <= 80:
            data['category'] = 'A'
        elif cumulative_percentage <= 95:
            data['category'] = 'B'
        else:
            data['category'] = 'C'
    
    return render(request, 'abc_analysis.html', {'analysis_data': sorted_data})

