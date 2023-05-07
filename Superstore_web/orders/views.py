from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .serializers import *
from .pagination import *
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
# Create your views here.

def loginPage(request):

    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)

        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            print("Hello")
            return redirect('index')
        else:
            messages.error(request, 'Username or Password is incorrect')

    context = {'form':form}
    return render(request,'orders/login.html',context)

@login_required(login_url='login')
def logoutPage(request):
    logout(request)
    return redirect('index')

def index(request):

    context = {'data':"Welcome TO Wow"}
    return render(request,'orders/index.html',context)

@login_required(login_url='login') 
def ListOrders(request):

    template = 'orders/show.html'
    table_title = 'Orders'
    create_object = 'Create Order'
    table_heading = (
        'Order ID',
        'Customer ID',
        'Order Date',
        'Status',
        'Action',
    )

    data = mm_order.objects.raw(
		'''select *, 
		if(DATE(ship_date) <= DATE(NOW()),"Delivered", "In Transit") as order_status  
		from mm_order orders
		left join mm_shipping_details ship
		on orders.order_id = ship.order_id
        order by orders.created_at desc
        limit 1000
        '''
	)

    table_data = []
    urls = []
    for entry in data:
        status = entry.order_status
        urls = [
                ['Order Details',entry.order_id,'View'],
                ['Delete Order', entry.order_id, 'Delete'],
            ]

        check =  entry.order_date + timedelta(days=30)
        # if status != 'Returned' and datetime.date(datetime.today()) < check:
        #     urls = [
        #             ['Order Details',entry.order_id,'View'],
        #             ['Delete Order', entry.order_id, 'Delete'],
        #             ['Return Order', entry.order_id, 'Return']
        #         ]
        if entry.return_status:
            status = 'Returned'
        
        table_data.append( [ 
           [
                entry.order_id,
                entry.customer_id.customer_id,
                entry.order_date,
                status,
            ],
            urls
            
        ])

    context = {
        'table_title': table_title,
        'create_object': create_object,
        'table_heading': table_heading,
        'table_data' : table_data,
    }

    return render(request, template , context)

@login_required(login_url='login') 
def ListProducts(request):

    template = 'orders/show.html'
    table_title = 'Products'
    create_object = 'Create Product'
    table_heading = (
        'Product ID',
        'Category',
        'Sub Category',
        'Product',
        'MRP',
        'Manufacturing',
        'Action',
    )
    
    data = mm_product.objects.all().order_by('-updated_at')[:1000]

    table_data = []
    urls = []
    for entry in data:
        table_data.append( [ 
            [
                entry.product_id ,
                entry.category_id.category,
                entry.sub_category_id.sub_category,
                entry.product_name,
                entry.mrp,
                entry.manu_cost,
            ],
            [
                ['Update Product',entry.product_id,'Edit'],
                ['Delete Product', entry.id, 'Delete'],
            ]
        ])
    context = {
        'table_title': table_title,
        'create_object': create_object,
        'table_heading': table_heading,
        'table_data' : table_data,
        'urls' : urls
    }
    return render(request, template , context) 

def ListCustomer(request):
    template = 'orders/show.html'
    table_title = 'Customers'
    create_object = 'Create Customer'
    table_heading = (
        'Customer ID',
        'Name',
        'Segment',
        'Action',
    )
    
    data = mm_customer.objects.all().order_by('-updated_at')[:1000]

    table_data = []
    urls = []
    for entry in data:
        table_data.append( [
            [ 
                entry.customer_id ,
                entry.first_name + " " + entry.last_name,
                entry.segment,
            ],
            [
                ['Customer Detail', entry.id,'View'],
                ['Update Customer', entry.id, 'Edit'],
                ['Delete Customer', entry.id, 'Delete'],
            ]
        ])
        
    context = {
        'table_title': table_title,
        'create_object': create_object,
        'table_heading': table_heading,
        'table_data' : table_data,
    }

    return render(request, template , context)

def ListCategory(request):

    template = 'orders/show.html'
    table_title = 'Category'
    create_object = 'Create Category'
    table_heading = (
        'ID',
        'Category',
        'Action',
    )

    data = mm_category.objects.all()
    table_data = []
    urls = []
    for entry in data:
        table_data.append( [ 
            [
                entry.category_id,
                entry.category,
            ],
            [
                ['Update Category',entry.category_id,'Edit'],
                ['Delete Category', entry.category_id, 'Delete'],
            ]  
        ])
        
    context = {
        'table_title': table_title,
        'create_object': create_object,
        'table_heading': table_heading,
        'table_data' : table_data,
    }

    return render(request, template, context)

def ListSubCategory(request):

    template = 'orders/show.html'
    table_title = 'Sub Category'
    create_object = 'Create Sub Category'
    table_heading = (
        'ID',
        'Category',
        'Sub Category',
        'Action',
    )

    data = mm_sub_category.objects.all()
    table_data = []
    urls = []
    for entry in data:
        table_data.append( [ 
            [
                entry.sub_category_id,
                entry.category_id.category,
                entry.sub_category,
            ],
            [
                ['Update Sub Category',entry.sub_category_id,'Edit'],
                ['Delete Sub Category', entry.sub_category_id, 'Delete'],
            ]
            
        ])
       
    context = {
        'table_title': table_title,
        'create_object': create_object,
        'table_heading': table_heading,
        'table_data' : table_data,
    }

    return render(request, template, context)

# def ListShipping(request):

#     template = 'orders/show.html'
#     table_title = 'Shipping Details'
#     table_heading = (
#         'ID',
#         'Category',
#         'Sub Category',
#         'Action',
#     )

#     data = mm_sub_category.objects.all()
#     table_data = []
#     urls = []
#     for entry in data:
#         table_data.append( [ 
#             [
#                 entry.sub_category_id,
#                 entry.category_id.category,
#                 entry.sub_category,
#             ],
#             [
#                 ['Update Sub Category',entry.sub_category_id,'Edit'],
#                 ['Delete Sub Category', entry.sub_category_id, 'Delete'],
#             ]
            
#         ])
       
#     context = {
#         'table_title': table_title,
#         'table_heading': table_heading,
#         'table_data' : table_data,
#     }

#     return render(request, template, context)

def CreateOrder(request):
    
    data = {}
    product_form = AddProductFormSet(queryset=mm_order_product.objects.none())
    
    if request.method == 'POST':
        product_form = AddProductFormSet(data=request.POST)
        customer_id = product_form.data['customer_id']
        customer = mm_customer.objects.get(customer_id = customer_id)
        # Check if submitted forms are valid
        if not customer:
            data = {
                "error" : "Invalid Customer ID",
                "product_form" : product_form
            }
            return render(request, 'orders/add_product.html', data)

        if product_form.is_valid():
            date = datetime.now()
            order_id = 'MM' + '-' + str(date.strftime("%Y")) + '-' + customer_id + '-' + str(date)[-5:]
            new_order = mm_order.objects.create(order_id=order_id, customer_id=customer)
            
            for form in product_form:
                mm_order_product.objects.create(
                    quantity = form.cleaned_data['quantity'], 
                    discount = form.cleaned_data['discount'], 
                    shipping_cost = form.cleaned_data['shipping_cost'],
                    order_id = new_order ,
                    product_id = form.cleaned_data['product_id'],
                )
            print("Hello")
            mm_shipping_details.objects.create(
                order_id=new_order,
                priority = product_form.data['priority'], 
                ship_date = product_form.data['ship_date'],
                ship_mode = product_form.data['ship_mode'],
            )

            return redirect('Order List')

    data = {
        "error" : "",
        "product_form" : product_form
    }

    return render(request, 'orders/add_product.html', data) 

@login_required(login_url='login')
def OrderDetials(request,pk):
    data = {}
    try:
        items = mm_order_product.objects.filter(order_id=pk)
    except:
        return mm_order.DoesNotExist()

    if request.method == "GET":
        context = []
        total = 0
        for item in items:
            item_total = (item.product_id.mrp * item.quantity )* (1 - item.discount) + item.shipping_cost 
            arr = {
                'product_name':item.product_id.product_name,
                'category':item.product_id.category_id.category,
                'sub_category':item.product_id.sub_category_id.sub_category,
                'discount':item.discount,
                'shipping_cost':item.shipping_cost,
                'mrp':item.product_id.mrp,
                'quantity':item.quantity,
                'total':item_total
            }
            total += item_total
            context.append(arr)

        print(context)
            
        data = {"data":context, "order_id":pk, "total" : total} 
                        
        return render(request, 'orders/order_details.html', data )

    if request.method == "PUT":
        ...

@login_required(login_url='login') 
def UpdateProduct(request, pk):
    product = mm_product.objects.get(product_id=pk)
    form = ProductForm(instance = product)
    
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('Product List')
    data = {'form': form}
    return render(request, 'orders/update.html', data)

@login_required(login_url='login') 
def CreateProduct(request):
    data = {}
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("Product List")
    
    data["form"] = form
    data["action"] = 'Create'
    return render(request, 'orders/product_details.html', data)

@login_required(login_url='login') 
def LoadSubCat(request):
    category_id = request.GET.get('id_category_id')
    print(category_id)
    sub_categories = mm_sub_category.objects.filter(category_id=category_id).order_by('sub_category')
    return render(request, 'orders/sub_dropdown_list.html', {'sub_categories':sub_categories})

# def AddProduct(request):
#     template = "orders/add_product.html"

#     # Define method to handle GET request
#     if request.method == 'GET':
#         # Create an instance of the formset
#         formset = AddProductFormSet(queryset=mm_order_product.objects.none())
#     elif request.method == 'POST':

#         formset = AddProductFormSet(data=request.POST)

#         # Check if submitted forms are valid
#         if formset.is_valid():
#             print(formset)
#             return redirect('Product List')

    # return render(request, template, {
    #     'formset':formset
    # })clear

# def CreateOrder(request):
#     data = {}
#     product_form = AddProductFormSet(queryset=mm_order_product.objects.none())

#     if request.method == 'POST':
#         product_form = AddProductFormSet(data=request.POST)
#         customer_id = product_form.data['customer_id']
#         customer = mm_customer.objects.get(customer_id = customer_id)
#         # Check if submitted forms are valid
#         if not customer:
#             data = {
#                 "error" : "Invalid Customer ID",
#                 "product_form" : product_form
#             }
#             return render(request, 'orders/add_product.html', data)

#         if product_form.is_valid():
#             date = datetime.now()
#             order_id = 'MM' + '-' + str(date.strftime("%Y")) + '-' + customer_id + '-' + str(date)[-5:]
#             new_order = mm_order.objects.create(order_id=order_id, customer_id=customer)
            
#             for form in product_form:
#                 mm_order_product.objects.create(
#                     quantity = form.cleaned_data['quantity'], 
#                     discount = form.cleaned_data['discount'], 
#                     shipping_cost = form.cleaned_data['shipping_cost'],
#                     order_id = new_order ,
#                     product_id = form.cleaned_data['product_id'],
#                 )
            
#             return redirect('Order List')

#     data = {
#         "error" : "",
#         "product_form" : product_form
#     }

#     return render(request, 'orders/add_product.html', data) 

       

def CustomerDetails(request,pk):
    data = {}
    try:
        addresses = mm_customer_address.objects.filter(customer_id=pk)
        customer =  mm_customer.objects.get(id=pk)
    except:
        return mm_customer.DoesNotExist()

    context = []
    
    for address in addresses:
        arr = {
            "City" : address.address_id.city ,
            "State" : address.address_id.add_state,
            "Country" : address.address_id.country,
            "Postal_Code" : address.postal_code,
            "ID" : address.pk
        }
        context.append(arr)
    data["data"] = {
        "address" : context,
        "customer" : customer,
    }
    return render(request, 'orders/customer_details.html', data )

def CreateAddress(request,customer_id):
    form = AddressForm()
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            entry = {
                'city': form.cleaned_data['city'],
                'add_state':form.cleaned_data['add_state'],
                'country':form.cleaned_data['country'],
                'region':form.cleaned_data['region'],
                'market': form.cleaned_data['market'],
            }

            check = mm_address.objects.filter(Q(city=entry['city']) & Q(add_state=entry['add_state'])).exists()
            print(check)
            if not check:
                form.save()
            
            address = mm_address.objects.get(Q(city=entry['city']) & Q(add_state=entry['add_state']))
            customer = mm_customer.objects.get(id=customer_id)
            print(address.address_id,customer_id,form.cleaned_data['postal_code'] )
            entry = {
                'id':int(mm_customer_address.objects.latest('id').id + 1),
                'address_id':address,
                'customer_id':customer_id,
                'postal_code':form.cleaned_data['postal_code'],
                }
            cust_add = mm_customer_address(id=int(mm_customer_address.objects.latest('id').id + 1),
                address_id=address,
                customer_id=customer,
                postal_code=form.cleaned_data['postal_code'])
            cust_add.save()
            return redirect('Customer Detail',pk=customer_id)
    data = {'form': form}
    return render(request, 'orders/update.html', data)

def CreateCustomer(request):
    form = CustomerForm()
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Customer List')
    data = {'form': form}
    return render(request, 'orders/update.html', data)

def UpdateCustomer(request,pk):
	customer = mm_customer.objects.get(id=pk)
	form = CustomerForm(instance = customer)

	if request.method == "POST":
		form = CustomerForm(request.POST, instance=customer)
		if form.is_valid():
			form.save()
			return redirect('Customer List')
	
	data = {'form': form}
	return render(request, 'orders/update.html', data)

def UpdateOrder(request,pk):
    ...

def DeleteOrder(request,pk):
    order = mm_order.objects.get(order_id=pk)
    items = mm_order_product.objects.filter(order_id=pk)
    ship = mm_shipping_details.objects.filter(order_id=pk)

    if items.exists() or ship.exists():
        messages.error(request, 'Order has Shipping or Items. Please delete it first.')
    else:
        order.delete()

    if request.user.is_superuser:
        items.delete()
        ship.delete()
        order.delete()

    return redirect('Order List') 

def DeleteCustomer(request,pk):
    order = mm_order.objects.filter(customer_id=pk)
    address = mm_customer_address.objects.filter(customer_id=pk)
    customer = mm_customer.objects.get(id=pk)
    
    if address.exists() or order.exists():
        messages.error(request, 'Customer has Address or Order. Please delete it first.')
    else:
        customer.delete()
    
    return redirect('Customer List')

def DeleteProduct(request, pk):
    items = mm_order_product.objects.filter(product_id=pk)
    product = mm_product.objects.filter(id=pk)
    if items.exists():
        messages.error(request,"Product In Use")
    else:
        product.delete()
    return redirect('Product List')

def DeleteItem(request,pk):
    Item = mm_order_product.objects.get(id=pk)
    Item.delete()
    return redirect('Order Detail',pk=Item.order_id)

def DeleteAddress(request,pk):
    address = mm_customer_address.objects.get(id=pk)
    address.delete()
    return redirect('Customer Detail',pk=address.customer_id.id)

def DeleteCategory(request,pk):
    product = mm_product.objects.filter(category_id=pk)
    data = mm_category.objects.get(category_id=pk)
    if product.exists():
        messages.error(request,"Product of this Category Exists")
    else:
        data.delete()
    return redirect('Category List')

def DeleteSubCategory(request,pk):
    product = mm_product.objects.filter(sub_category_id=pk)
    data = mm_sub_category.objects.get(sub_category_id=pk)
    if product.exists():
        messages.error(request,"Product of this Sub Category Exists")
    else:
        data.delete()
    return redirect('Sub Category List')

def Shipping(request):

    template = 'orders/show.html'
    create_object = 'Create Order'
    table_title = 'Shipping'
    table_heading = (
        'Shipping Id',
        'Order ID',
        'Ship Date',
        'Priority',
        'Mode'
    )

    data = mm_shipping_details.objects.all().order_by('-created_at')[:1000]

    table_data = []
    for entry in data:
        table_data.append( [ 
           [
                entry.ship_id,
                entry.order_id.order_id,
                entry.ship_date,
                entry.priority,
                entry.ship_mode
            ]

        ])

    context = {
        'table_title': table_title,
        'create_object': create_object,
        'table_heading': table_heading,
        'table_data' : table_data,
    }

    return render(request, template , context)

def CreateCategory(request):
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Category List')
    data = {'form': form}
    return render(request, 'orders/update.html', data)

def CreateSubCategory(request):
    form = SubCategoryForm()
    if request.method == "POST":
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Sub Category List')
    data = {'form': form}
    return render(request, 'orders/update.html', data)

def UpdateCategory(request,pk):
    record = mm_category.objects.get(category_id=pk)
    form = CategoryForm(instance = record)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('Category List')
    data = {'form': form}
    return render(request, 'orders/update.html', data)

def UpdateSubCategory(request,pk):
    record = mm_sub_category.objects.get(sub_category_id=pk)
    form = SubCategoryForm(instance = record)
    if request.method == "POST":
        form = SubCategoryForm(request.POST,instance = record)
        if form.is_valid():
            form.save()
            return redirect('Sub Category List')
    data = {'form': form}
    return render(request, 'orders/update.html', data)
    
def RegisterEmployee(request):
    # print(request)
    form = CreateUser()
    # permission = Permission.objects.filter(codename__in=employee_permission).all()

    if request.method == 'POST':            
        form = CreateUser(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            # user_group, created = Group.objects.get_or_create(name='staff')
            # user.is_staff = True
            user.save()
            # user.groups.add(user_group)
            # user_group.permissions.set(permission)
            return redirect('Employee List')
        else:
            messages.error(request, 'An error occured during registration')

    context = {'form':form, 'title':'Register Employee'}
    return render(request, 'orders/register.html', context)

def EmployeeList(request):
    # template = 'orders/show.html'
    # table_title = 'Users'
    # create_object = 'Create User'
    # table_heading = (
    #     'ID',
    #     'Category',
    #     'Action',
    # )
    users = get_user_model()
    data = users.objects.all()
    context = {'data':data}
    return render(request,'orders/employee.html',context)


def ReturnOrder(request, pk):
    order = mm_order.objects.filter(order_id=pk)
    order.update(return_status= True)
    return redirect('Order List')