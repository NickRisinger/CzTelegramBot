/*
  Warnings:

  - The primary key for the `Code` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `id` on the `Code` table. All the data in the column will be lost.
  - The primary key for the `Tread` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `id` on the `Tread` table. All the data in the column will be lost.
  - The primary key for the `User` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `id` on the `User` table. All the data in the column will be lost.

*/
-- RedefineTables
PRAGMA defer_foreign_keys=ON;
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_Code" (
    "content" TEXT NOT NULL PRIMARY KEY,
    "user_tg_id" INTEGER NOT NULL,
    CONSTRAINT "Code_user_tg_id_fkey" FOREIGN KEY ("user_tg_id") REFERENCES "User" ("tg_id") ON DELETE RESTRICT ON UPDATE CASCADE
);
INSERT INTO "new_Code" ("content", "user_tg_id") SELECT "content", "user_tg_id" FROM "Code";
DROP TABLE "Code";
ALTER TABLE "new_Code" RENAME TO "Code";
CREATE UNIQUE INDEX "Code_content_key" ON "Code"("content");
CREATE TABLE "new_Tread" (
    "tread_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "user_tg_id" INTEGER NOT NULL,
    CONSTRAINT "Tread_user_tg_id_fkey" FOREIGN KEY ("user_tg_id") REFERENCES "User" ("tg_id") ON DELETE RESTRICT ON UPDATE CASCADE
);
INSERT INTO "new_Tread" ("tread_id", "user_tg_id") SELECT "tread_id", "user_tg_id" FROM "Tread";
DROP TABLE "Tread";
ALTER TABLE "new_Tread" RENAME TO "Tread";
CREATE UNIQUE INDEX "Tread_tread_id_key" ON "Tread"("tread_id");
CREATE UNIQUE INDEX "Tread_user_tg_id_key" ON "Tread"("user_tg_id");
CREATE TABLE "new_User" (
    "tg_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "points" INTEGER NOT NULL DEFAULT 0,
    "created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO "new_User" ("created_at", "points", "tg_id") SELECT "created_at", "points", "tg_id" FROM "User";
DROP TABLE "User";
ALTER TABLE "new_User" RENAME TO "User";
CREATE UNIQUE INDEX "User_tg_id_key" ON "User"("tg_id");
PRAGMA foreign_keys=ON;
PRAGMA defer_foreign_keys=OFF;
