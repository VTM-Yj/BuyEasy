# addresses/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Address
from .forms import AddressForm
from .decorators import session_login_required

@session_login_required
def address_list(request):
    user_id = request.session.get('user_id')
    addresses = Address.objects.filter(user_id=user_id)
    return render(request, 'address_list.html', {'addresses': addresses})


@session_login_required
def address_add(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user_id = request.session.get('user_id')  # 从 session 中获取用户ID
            address.save()
            return redirect('address_list')
    else:
        form = AddressForm()
    return render(request, 'address_form.html', {'form': form})

@session_login_required
def address_edit(request, pk):
    user_id = request.session.get('user_id')
    address = get_object_or_404(Address, pk=pk, user_id=user_id)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('address_list')
    else:
        form = AddressForm(instance=address)
    return render(request, 'address_form.html', {'form': form})

@session_login_required
def address_delete(request, pk):
    user_id = request.session.get('user_id')
    address = get_object_or_404(Address, pk=pk, user_id=user_id)
    if request.method == 'POST':
        address.delete()
        return redirect('address_list')
    return render(request, 'address_confirm_delete.html', {'object': address})
