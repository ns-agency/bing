import Vue from 'vue'
import Router from 'vue-router'
import Login from './views/Login.vue'
import Home from './views/Home.vue'
import Prism from './views/Prism.vue'
import auth from './middleware/auth'
Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home,
      meta: {
        middleware: auth,
      }
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/staff/prism',
      name: 'prism',
      component: Prism
    }
  ]
});

/* STOLEN FROM https://markus.oberlehner.net/blog/implementing-a-simple-middleware-with-vue-router/ */
function nextFactory(context, middleware, index) {
  const subsequentMiddleware = middleware[index];
  // If no subsequent Middleware exists,
  // the default `next()` callback is returned.
  if (!subsequentMiddleware) return context.next;

  return (...parameters) => {
    // Run the default Vue Router `next()` callback first.
    context.next(...parameters);
    // Then run the subsequent Middleware with a new
    // `nextMiddleware()` callback.
    const nextMiddleware = nextFactory(context, middleware, index + 1);
    subsequentMiddleware({ ...context, next: nextMiddleware });
  };
}

router.beforeEach((to, from, next) => {
  if (to.meta.middleware) {
    const middleware = Array.isArray(to.meta.middleware)
      ? to.meta.middleware
      : [to.meta.middleware];

    const context = {
      from,
      next,
      router,
      to,
    };
    const nextMiddleware = nextFactory(context, middleware, 1);

    return middleware[0]({ ...context, next: nextMiddleware });
  }

  return next();
});

export default router;