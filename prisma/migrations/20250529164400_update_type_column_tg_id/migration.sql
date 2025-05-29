/*
  Warnings:

  - You are about to alter the column `user_tg_id` on the `codes` table. The data in that column could be lost. The data in that column will be cast from `Int` to `BigInt`.
  - The primary key for the `treads` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to alter the column `tread_id` on the `treads` table. The data in that column could be lost. The data in that column will be cast from `Int` to `BigInt`.
  - You are about to alter the column `user_tg_id` on the `treads` table. The data in that column could be lost. The data in that column will be cast from `Int` to `BigInt`.
  - The primary key for the `users` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to alter the column `tg_id` on the `users` table. The data in that column could be lost. The data in that column will be cast from `Int` to `BigInt`.

*/
-- RedefineTables
PRAGMA defer_foreign_keys=ON;
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_codes" (
    "content" TEXT NOT NULL PRIMARY KEY,
    "user_tg_id" BIGINT NOT NULL,
    CONSTRAINT "codes_user_tg_id_fkey" FOREIGN KEY ("user_tg_id") REFERENCES "users" ("tg_id") ON DELETE RESTRICT ON UPDATE CASCADE
);
INSERT INTO "new_codes" ("content", "user_tg_id") SELECT "content", "user_tg_id" FROM "codes";
DROP TABLE "codes";
ALTER TABLE "new_codes" RENAME TO "codes";
CREATE UNIQUE INDEX "codes_content_key" ON "codes"("content");
CREATE TABLE "new_treads" (
    "tread_id" BIGINT NOT NULL PRIMARY KEY,
    "user_tg_id" BIGINT NOT NULL,
    CONSTRAINT "treads_user_tg_id_fkey" FOREIGN KEY ("user_tg_id") REFERENCES "users" ("tg_id") ON DELETE RESTRICT ON UPDATE CASCADE
);
INSERT INTO "new_treads" ("tread_id", "user_tg_id") SELECT "tread_id", "user_tg_id" FROM "treads";
DROP TABLE "treads";
ALTER TABLE "new_treads" RENAME TO "treads";
CREATE UNIQUE INDEX "treads_tread_id_key" ON "treads"("tread_id");
CREATE UNIQUE INDEX "treads_user_tg_id_key" ON "treads"("user_tg_id");
CREATE TABLE "new_users" (
    "tg_id" BIGINT NOT NULL PRIMARY KEY,
    "points" INTEGER NOT NULL DEFAULT 0,
    "created_at" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO "new_users" ("created_at", "points", "tg_id") SELECT "created_at", "points", "tg_id" FROM "users";
DROP TABLE "users";
ALTER TABLE "new_users" RENAME TO "users";
CREATE UNIQUE INDEX "users_tg_id_key" ON "users"("tg_id");
PRAGMA foreign_keys=ON;
PRAGMA defer_foreign_keys=OFF;
