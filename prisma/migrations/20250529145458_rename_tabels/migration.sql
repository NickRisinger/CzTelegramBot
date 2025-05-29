/*
  Warnings:

  - You are about to drop the `Code` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `Tread` table. If the table is not empty, all the data it contains will be lost.
  - You are about to drop the `User` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropTable
PRAGMA foreign_keys=off;
DROP TABLE "Code";
PRAGMA foreign_keys=on;

-- DropTable
PRAGMA foreign_keys=off;
DROP TABLE "Tread";
PRAGMA foreign_keys=on;

-- DropTable
PRAGMA foreign_keys=off;
DROP TABLE "User";
PRAGMA foreign_keys=on;

-- CreateTable
CREATE TABLE "users" (
    "tg_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "points" INTEGER NOT NULL DEFAULT 0,
    "created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- CreateTable
CREATE TABLE "codes" (
    "content" TEXT NOT NULL PRIMARY KEY,
    "user_tg_id" INTEGER NOT NULL,
    CONSTRAINT "codes_user_tg_id_fkey" FOREIGN KEY ("user_tg_id") REFERENCES "users" ("tg_id") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "treads" (
    "tread_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "user_tg_id" INTEGER NOT NULL,
    CONSTRAINT "treads_user_tg_id_fkey" FOREIGN KEY ("user_tg_id") REFERENCES "users" ("tg_id") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateIndex
CREATE UNIQUE INDEX "users_tg_id_key" ON "users"("tg_id");

-- CreateIndex
CREATE UNIQUE INDEX "codes_content_key" ON "codes"("content");

-- CreateIndex
CREATE UNIQUE INDEX "treads_tread_id_key" ON "treads"("tread_id");

-- CreateIndex
CREATE UNIQUE INDEX "treads_user_tg_id_key" ON "treads"("user_tg_id");
