const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
).replace(/\/$/, '');

async function request(path, options = {}) {
  let response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      headers: {
        ...(options.body ? { 'Content-Type': 'application/json' } : {}),
        ...options.headers,
      },
    });
  } catch {
    throw new Error(
      'Could not connect to the allocation server. Please try again.'
    );
  }

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    const error = new Error(
      data.message || data.detail || 'Something went wrong. Please try again.'
    );
    error.status = response.status;
    error.code = data.code;
    throw error;
  }

  return data;
}

export function registerStudent({ name, indexNumber }) {
  return request('/api/register/', {
    method: 'POST',
    body: JSON.stringify({
      full_name: name,
      index_number: indexNumber,
    }),
  });
}

export function findStudent(indexNumber) {
  return request(`/api/student/${encodeURIComponent(indexNumber)}/`);
}

export function getGroups() {
  return request('/api/groups/');
}
