from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Ad, ExchangeProposal
from .forms import AdForm, ProposalForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.db import transaction

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Автоматический вход после регистрации
            return redirect('list_ads')
    else:
        form = UserCreationForm()
    return render(request, 'ads/register.html', {'form': form})



@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user  # Привязываем объявление к текущему пользователю
            ad.save()
            messages.success(request, 'Объявление успешно создано!')
            return redirect('ad_detail', ad_id=ad.id)
    else:
        form = AdForm()
    return render(request, 'ads/create_ad.html', {'form': form})

@login_required
def edit_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.user != request.user:  # Проверка авторства
        messages.error(request, 'Вы не можете редактировать это объявление!')
        return redirect('list_ads', ad_id=ad.id)

    if request.method == 'POST':
        form = AdForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объявление обновлено!')
            return redirect('ad_detail', ad_id=ad.id)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/ad_form.html', {'form': form, 'ad': ad})

@login_required
def delete_ad(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.user != request.user:
        messages.error(request, 'У вас нет прав на удаление!')
        return redirect('list_ads')

    ad.delete()
    messages.success(request, 'Объявление удалено.')
    return redirect('list_ads')

def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    proposals = ExchangeProposal.objects.filter(ad_receiver=ad).select_related('ad_sender__user')
    return render(request, 'ads/ad_detail.html', {
        'ad': ad,
        'proposals': proposals,
    })




@login_required
def send_proposal(request, ad_id):
    ad_receiver = get_object_or_404(Ad, id=ad_id)

    if not Ad.objects.filter(user=request.user).exists():
        messages.error(request, 'У вас нет товаров для обмена!')
        return redirect('list_ads')

    if request.method == 'POST':
        form = ProposalForm(request.POST, user=request.user)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.ad_receiver = ad_receiver
            proposal.created_by = request.user
            proposal.save()
            messages.success(request, 'Предложение отправлено!')
            return redirect('ad_detail', ad_id=ad_receiver.id)
    else:
        form = ProposalForm(user=request.user)

    return render(request, 'ads/send_proposal.html', {
        'form': form,
        'ad_receiver': ad_receiver,
    })





@login_required
def update_proposal_status(request, proposal_id, status):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id)
    if proposal.ad_receiver.user != request.user:  # Только получатель может менять статус
        messages.error(request, 'Недостаточно прав!')
        return redirect('ad_detail', ad_id=proposal.ad_receiver.id)

    if status in ['accepted', 'rejected']:
        proposal.status = status
        proposal.save()
        messages.success(request, f'Предложение {proposal.get_status_display()}!')
    return redirect('ad_detail', ad_id=proposal.ad_receiver.id)

def list_ads(request):
    ads_list = Ad.objects.all().order_by('-created_at')
    category = request.GET.get('category')
    condition = request.GET.get('condition')
    search_query = request.GET.get('q')

    if search_query:
        ads_list = ads_list.filter(title__icontains=search_query) | ads_list.filter(description__icontains=search_query)
    if category:
        ads_list = ads_list.filter(category__iexact=category)
    if condition:
        ads_list = ads_list.filter(condition__iexact=condition)

    paginator = Paginator(ads_list, 10)  # 10 объявлений на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'ads/list_ads.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'Ad' : Ad
    })


@login_required
@require_POST
def accept_proposal(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id)

    if proposal.ad_receiver.user != request.user:
        messages.error(request, "Вы не можете принять это предложение — вы не владелец товара.")
        return redirect('ad_detail', ad_id=proposal.ad_receiver.id)

    if proposal.status != 'pending':
        messages.error(request, "Это предложение уже обработано.")
        return redirect('ad_detail', ad_id=proposal.ad_receiver.id)

    with transaction.atomic():
        # Меняем владельцев у товаров
        ad_sender = proposal.ad_sender
        ad_receiver = proposal.ad_receiver

        owner_sender = ad_sender.user
        owner_receiver = ad_receiver.user

        ad_sender.user = owner_receiver
        ad_receiver.user = owner_sender

        ad_sender.save()
        ad_receiver.save()

        # Обновляем статус предложения
        proposal.status = 'accepted'
        proposal.save()

        # Можно дополнительно отклонить другие предложения на этот товар
        ExchangeProposal.objects.filter(ad_receiver=ad_receiver).exclude(id=proposal.id).update(status='rejected')

    messages.success(request, "Обмен успешно выполнен!")

    return redirect('ad_detail', ad_id=ad_receiver.id)



def about(request):
    return render(request, 'ads/about.html')

def rules(request):
    return render(request, 'ads/rules.html')

def contacts(request):
    return render(request, 'ads/contacts.html')

def faq(request):
    return render(request, 'ads/faq.html')
