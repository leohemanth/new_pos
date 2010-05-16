#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,get_object_or_404
from models import Menu, Category, Article

def get_path(request, path='home', template='page.html', prefix='/'):
    if path:
        cat = Category.objects.filter(path=path,subdomain=request.subdomain)
        if cat.count() == 0:
            article = get_object_or_404(Article,path=path,subdomain=request.subdomain)
            articles = [article,]
            cat = article.parent
            context = {'articles':articles}
        else:
            cat = cat[0]
            articles = cat.articles()
            context = {'category':cat, 'articles':articles}
        select_list = [cat.slug,]
        cat_parent = cat.parent
        while cat_parent:
            select_list.append(cat_parent.slug)
            cat_parent = cat_parent.parent
    else:
        context = {}
        select_list = ()
    # root nenus
    menus = Menu.objects.all()
    for menu in menus:
        menu.update_selection(select_list)
        context[menu.name] = menu
    context['prefix'] = prefix
    context['user'] = request.user
    return render_to_response(template, context)


def plan(request, template='plan.html', prefix='/'):
    categories = Category.objects.filter(parent__isnull=True, order__gt=0,subdomain=request.subdomain).order_by('order')
    context = {'categories':categories, 'prefix':prefix}
    # root nenus
    menus = Menu.objects.filter(subdomain=request.subdomain)
    for menu in menus:
        context[menu.name] = menu
    return render_to_response(template, context)