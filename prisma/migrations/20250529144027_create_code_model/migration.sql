-- CreateTable
CREATE TABLE "Code" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "content" TEXT NOT NULL,
    "user_tg_id" INTEGER NOT NULL,
    CONSTRAINT "Code_user_tg_id_fkey" FOREIGN KEY ("user_tg_id") REFERENCES "User" ("tg_id") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateIndex
CREATE UNIQUE INDEX "Code_content_key" ON "Code"("content");
