// utils.js
export function getUserId() {
  let uid = localStorage.getItem("user_id");
  if (!uid) {
    uid = crypto.randomUUID();
    localStorage.setItem("user_id", uid);
  }
  return uid;
}
