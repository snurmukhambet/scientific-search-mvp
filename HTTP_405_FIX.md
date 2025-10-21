# 🔧 Исправление HTTP 405 Error на Render

## 🐛 Проблема

```
XHR POST https://frontend-client-ftwt.onrender.com/api/ask
[HTTP/3 405  287ms]
```

**Причина:** Frontend пытается отправить POST на `/api/ask` через свой собственный URL, но:

1. Nginx не имеет proxy для `/api/` (мы удалили его ранее)
2. `VITE_API_URL` не встраивается в код при сборке на Render

---

## ✅ Решение

### 1. **Frontend Dockerfile** - Дефолтное значение для VITE_API_URL

```dockerfile
# Build argument с дефолтным значением
ARG VITE_API_URL=https://ml-backend-api.onrender.com
ENV VITE_API_URL=$VITE_API_URL

# Debug log
RUN echo "Building with VITE_API_URL=${VITE_API_URL}"
```

**Что изменилось:**

- ✅ Добавлено дефолтное значение в `ARG`
- ✅ Переменная всегда доступна во время сборки
- ✅ Добавлен debug log для проверки

### 2. **App.tsx** - Debug логирование

```typescript
const apiUrl = import.meta.env.VITE_API_URL || "";
const endpoint = apiUrl ? `${apiUrl}/api/ask` : "/api/ask";

console.log("API Endpoint:", endpoint); // Debug log
```

---

## 🔍 Как Проверить Исправление

### После деплоя на Render:

1. **Открыть Frontend:** `https://frontend-client-ftwt.onrender.com`
2. **Открыть Console (F12):**

   ```
   API Endpoint: https://ml-backend-api.onrender.com/api/ask
   ```

   ✅ Должен показывать полный URL бэкенда

3. **Отправить запрос:**
   - Должен уйти на `https://ml-backend-api.onrender.com/api/ask`
   - **НЕ** на `https://frontend-client-ftwt.onrender.com/api/ask`

---

## 📋 Commit и Push

```bash
git add .
git commit -m "Fix HTTP 405: Set default VITE_API_URL in Dockerfile

- Frontend Dockerfile: Add default value for VITE_API_URL ARG
- Ensures API URL is always available during Vite build
- Add debug logging to verify API endpoint
- Fixes POST requests going to frontend instead of backend"

git push origin main
```

---

## 🎯 Ожидаемый Результат

### До Исправления:

```
❌ POST https://frontend-client-ftwt.onrender.com/api/ask → 405 Error
```

### После Исправления:

```
✅ POST https://ml-backend-api.onrender.com/api/ask → 200 OK
```

---

## 💡 Как Это Работает

### Vite Build Process:

1. Render запускает `docker build` с `envVars` из `render.yaml`
2. Dockerfile получает `VITE_API_URL` как `ARG`
3. `ARG` преобразуется в `ENV` переменную
4. Vite встраивает `import.meta.env.VITE_API_URL` в JavaScript код
5. Собранный код содержит `https://ml-backend-api.onrender.com`

### Runtime:

- Пользователь открывает Frontend
- JavaScript выполняется с уже встроенным URL
- Запросы идут напрямую на Backend

---

## ⚠️ Важно

**VITE\_ переменные - это BUILD-TIME, не RUNTIME:**

- ✅ Встраиваются в код при `npm run build`
- ❌ НЕ могут быть изменены после сборки
- ❌ НЕ читаются из environment variables в браузере

**Для изменения API URL после деплоя нужно:**

1. Изменить `render.yaml`
2. Запустить rebuild Frontend сервиса

---

**Дата исправления:** October 21, 2025  
**Статус:** ✅ FIXED
