-- CreateTable
CREATE TABLE "Tread" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "tread_id" INTEGER NOT NULL,
    "user_tg_id" INTEGER NOT NULL,
    CONSTRAINT "Tread_user_tg_id_fkey" FOREIGN KEY ("user_tg_id") REFERENCES "User" ("tg_id") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateIndex
CREATE UNIQUE INDEX "Tread_tread_id_key" ON "Tread"("tread_id");

-- CreateIndex
CREATE UNIQUE INDEX "Tread_user_tg_id_key" ON "Tread"("user_tg_id");
