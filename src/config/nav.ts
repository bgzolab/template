// src/config/nav.ts
// 导航栏
export const navLinks = [
  { name: "Home", path: "/" },
  // 暂时重定向到外部站点，待后续迁移完成再恢复内部路由
  { name: "Blog", path: "https://blog.bgzo.cc/", external: true },
  { name: "Talks", path: "https://cast.bgzo.cc/", external: true },
  // Online tools
  { name: "Tools", path: "/tools" },
  // Playground
  { name: "Labs", path: "/labs" },
];
