import dao
from gkwebs.models import Category, Product, UserRole, Tag
from gkwebs import db, app, login
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import redirect, request
from flask_login import logout_user, current_user
from wtforms import TextAreaField
from wtforms.widgets import TextArea



class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN




class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class ProductView(AuthenticatedModelView):
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    can_view_details = True
    can_export = True
    column_export_list = ['id', 'name', 'price']
    column_exclude_list = ['image']
    column_labels = {
        'name' : 'Chuyến đi',
        'description': 'Mô tả',
        'price' : 'giá vé',

    }
    page_size = 3
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description' : CKTextAreaField
    }
class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        stats = dao.count_product_by_cate()
        return self.render('admin/index.html', stats=stats)
# class StartsView(AuthenticatedView):
#     @expose('/')
#     def index(self):
#         stats = dao.stats_revenue()
#         return self.render('admin/starts.html', stats=stats)
class StatsView(AuthenticatedView):
    @expose('/')
    def index(self):
        stats = dao.stats_revenue(kw=request.args.get('kw'),
                                  from_date=request.args.get('from_date'),
                                  to_date=request.args.get('to_date'))
        return self.render('admin/starts.html', stats=stats)


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')
admin = Admin(app, name=' Quản trị bán vé', template_mode='bootstrap4', index_view=MyAdminView())
admin.add_view(AuthenticatedModelView(Category, db.session, name = 'Danh mục'))
admin.add_view(AuthenticatedModelView(Tag, db.session, name = 'Tag'))
admin.add_view(ProductView(Product, db.session, name='Chuyến Đi'))
admin.add_view(StatsView(name='THỐNG KÊ - BÁO CÁO'))
admin.add_view(LogoutView(name='Đăng xuất'))