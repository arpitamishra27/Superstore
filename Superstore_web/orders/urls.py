from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path('login',views.loginPage,name='login'),
	path('logout',views.logoutPage,name='logout'),

	path('', views.index, name='index'),

	path('password-reset/',
		auth_views.PasswordResetView.as_view(
			template_name='orders/password_reset.html'
		),
		name='password_reset'),
	path('password-reset/done/',
		auth_views.PasswordResetDoneView.as_view(
			template_name='orders/password_reset_done.html'
		),
		name='password_reset_done'),
	path('password-reset-confirm/<uidb64>/<token>/',
		auth_views.PasswordResetConfirmView.as_view(
			template_name='orders/password_reset_confirm.html'
		),
		name='password_reset_confirm'),
	path('password-reset-complete/',
		auth_views.PasswordResetCompleteView.as_view(
			template_name='orders/password_reset_complete.html'
		),
		name='password_reset_complete'), 

	path('orders/<str:pk>/', views.OrderDetials, name='Order Details'),
	path('orders/',views.ListOrders,name="Order List"),
	path('products/', views.ListProducts, name="Product List"),
	path('customers/',views.ListCustomer, name="Customer List"),
	path('customers/<str:pk>/', views.CustomerDetails, name="Customer Detail"),
	path('new_order/',views.CreateOrder, name="Create Order"),
	path('new_product/', views.CreateProduct, name="Create Product"),
	path('new_address/',views.CreateAddress, name="Create Address"),
	path('product/<str:pk>/', views.UpdateProduct, name="Update Product"),
	path('update_customer/<str:pk>',views.UpdateCustomer,name="Update Customer"),
	path('update_order/<str:pk>',views.UpdateOrder,name="Update Order"),
	path('delete_order/<str:pk>',views.DeleteOrder, name="Delete Order"),
	path('delete_cusotmer/<str:pk>', views.DeleteCustomer, name="Delete Customer"),
	path('delete_product/<str:pk>',views.DeleteProduct,name="Delete Product"),
	path('new_address/<str:customer_id>', views.CreateAddress, name="Create Address"),
	path('delete_address/<str:pk>', views.DeleteAddress, name="Delete Address"),
	path('new_customer/', views.CreateCustomer, name="Create Customer"),
	path('register_employee/', views.RegisterEmployee, name='register_employee'),
	path('employees/',views.EmployeeList, name="Employee List"),

	path('new_category/',views.CreateCategory, name="Create Category"),
	path('new_sub_category/',views.CreateSubCategory, name="Create Sub Category"),
	path('delete_category/<str:pk>',views.DeleteCategory, name="Delete Category"),
	path('delete_sub_category/<str:pk>',views.DeleteSubCategory, name="Delete Sub Category"),
	path('category/',views.ListCategory,name="Category List"),
	path('subcategory/',views.ListSubCategory,name="Sub Category List"),
	path('update_subcategory/<str:pk>',views.UpdateSubCategory,name="Update Sub Category"),
	path('update_category/<str:pk>',views.UpdateCategory,name="Update Category"),
	path('return_order/<str:pk>', views.ReturnOrder,name="Return Order"),
	path('shipping/',views.Shipping, name="Ship List"),


	path('ajax/load_sub/', views.LoadSubCat, name='ajax_load_sub'),
	
]