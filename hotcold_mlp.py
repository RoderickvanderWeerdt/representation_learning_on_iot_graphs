from torch import nn
import pandas as pd

from workhours_dataset import Emb_Workhours_Dataset, ToTensor
from torch.utils.data import DataLoader
import torch

def shuffle_dataset(dataset_fn, shuffled_fn="shuffled_dataset.csv"):
    df = pd.read_csv(dataset_fn, sep=",")
    df = df.sample(frac=1).reset_index(drop=True)
    df.to_csv("shuffled_dataset.csv", index=False)


def perform_prediction(dataset_fn, show_all, save_model=False, embeddings_or_features=1, use_all=False, target_class=None): #embeddings=1, features=2, both=3
    if not use_all:
        shuffle_dataset(dataset_fn)
        if embeddings_or_features == 1:
            training_data = Emb_Workhours_Dataset(csv_file="shuffled_dataset.csv", train=True, transform=ToTensor(), target_class=target_class)
            test_data = Emb_Workhours_Dataset(csv_file="shuffled_dataset.csv", train=False, transform=ToTensor(), target_class=target_class)
    #     elif embeddings_or_features == 2:
    #         training_data = Features_Hotcold_Dataset(csv_file="shuffled_dataset.csv", train=True, transform=ToTensor())
    #         test_data = Features_Hotcold_Dataset(csv_file="shuffled_dataset.csv", train=False, transform=ToTensor())
    #     elif embeddings_or_features == 3:
    #         training_data = Emb_Feat_Hotcold_Dataset(csv_file="shuffled_dataset.csv", train=True, transform=ToTensor())
    #         test_data = Emb_Feat_Hotcold_Dataset(csv_file="shuffled_dataset.csv", train=False, transform=ToTensor())
    # else:
    #     train_set_fn = dataset_fn
    #     test_set_fn = "data/update_exp/THURSDAY/large_german_w_labels_THURSDAY_for_update_combined.csv"
    #     if embeddings_or_features == 1:
    #         shuffle_dataset(train_set_fn)
    #         training_data = Emb_Hotcold_Dataset(csv_file="shuffled_dataset.csv", transform=ToTensor(), train_all=True, emb_header="emb")
    #         shuffle_dataset(test_set_fn)
    #         test_data = Emb_Hotcold_Dataset(csv_file="shuffled_dataset.csv", transform=ToTensor(), train_all=True, emb_header="trained_emb")
    #     if embeddings_or_features == 2:
    #         shuffle_dataset(train_set_fn)
    #         training_data = Features_Hotcold_Dataset(csv_file="shuffled_dataset.csv", transform=ToTensor(), train_all=True)
    #         shuffle_dataset(test_set_fn)
    #         test_data = Features_Hotcold_Dataset(csv_file="shuffled_dataset.csv", transform=ToTensor(), train_all=True)
    #     if embeddings_or_features == 3:
    #         shuffle_dataset(train_set_fn)
    #         training_data = Emb_Feat_Hotcold_Dataset(csv_file="shuffled_dataset.csv", transform=ToTensor(), train_all=True, emb_header="emb")
    #         shuffle_dataset(test_set_fn)
    #         test_data = Emb_Feat_Hotcold_Dataset(csv_file="shuffled_dataset.csv", transform=ToTensor(), train_all=True, emb_header="trained_emb")

    batch_size = 4
    
    

    # Create data loaders.
    train_dataloader = DataLoader(training_data, batch_size=batch_size)
    test_dataloader = DataLoader(test_data, batch_size=batch_size)
    
    train_tss = []
    test_tss = []
    embedding_size = 0
    for sample in test_dataloader:
        X = sample['embedding']
        y = sample['target_class']
        embedding_size = X.shape[1]
        if show_all: print("Shape of X: ", X.shape)
        if show_all: print("Shape of y: ", y.shape, y.dtype)
        break

    # exit()

    # Get cpu or gpu device for training.
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if show_all: print("Using {} device".format(device))

    # Define model
    class NeuralNetwork(nn.Module):
        def __init__(self, x_size):
            super(NeuralNetwork, self).__init__()
            self.flatten = nn.Flatten()
            self.linear_relu_stack = nn.Sequential(
                nn.Linear(x_size, 512),
                nn.ReLU(),
                nn.Linear(512, 512),
                nn.ReLU(),
                nn.Linear(512, 2)
            )

        def forward(self, x):
            x = self.flatten(x)
            logits = self.linear_relu_stack(x)
            # logits = nn.functional.softmax(logits)
            return logits

    model = NeuralNetwork(embedding_size).to(device)
    model = model.float()
    if show_all: print(model)


    loss_fn = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)


    def train(dataloader, model, loss_fn, optimizer):
        size = len(dataloader.dataset)
        model.train()
        total = 0
        correct = 0
        for batch, sample in enumerate(dataloader):
            X = sample['embedding']
            y = sample['target_class']
            X, y = X.to(device), y.to(device)
            
            train_tss.append(y)

            # Compute prediction error
            pred = model(X.float())
            loss = loss_fn(pred.float(), y)
            _, predicted = torch.max(pred.data, 1)
            total += y.size(0)
            correct += (predicted == y).sum().item()
            # print(batch)
            # print(predicted, y)
            
            # Backpropagation
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if batch % 100 == 0:
                loss, current = loss.item(), batch * len(X)
                if show_all: print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")
                # print("x", X[0], "y", y[0], "pred", pred[0])
                # print("x", X[0], "y", torch.round(y[0]), "pred", torch.round(pred[0]))
        
        correct /= total
        if show_all: print(f"Train Accuracy: {(100*correct):>0.1f}%")
        return correct


    def test(dataloader, model, loss_fn):
        num_batches = len(dataloader)
        model.eval()
        total = 0
        correct = 0
        predicted_distribution = 0
        real_distribution = 0
        with torch.no_grad():
            for sample in dataloader:
                X = sample['embedding']
                y = sample['target_class']
                X, y = X.to(device), y.to(device)
                test_tss.append(y)
                pred = model(X.float())
                _, predicted = torch.max(pred.data, 1)
#                 print(predicted[0],y[0])
                total += y.size(0)
                correct += (predicted == y).sum().item()
                predicted_distribution += predicted.sum().item()
                real_distribution += y.sum().item()
        correct /= total
        if show_all: print(f"Test Accuracy: {(100*correct):>0.1f}%")
        if show_all: print(f"prediction distribution: {predicted_distribution} / {total-predicted_distribution} -- real distribution: {real_distribution} / {total}")
        return correct

    epochs = 20
    model = model.float()
    test_res = []
    train_res = []
    for t in range(epochs):
        if show_all: print(f"Epoch {t+1}\n-------------------------------")
        train_res.append(train(train_dataloader, model, loss_fn, optimizer))
        test_res.append(test(test_dataloader, model, loss_fn))
    if show_all: print("Done!")
    # else: print(f"Train Accuracy: {(100*train_res[-1]):>0.1f}, Test Accuracy: {(100*test_res[-1]):>0.1f}")
    print(f"Train Accuracy: {(100*train_res[-1]):>0.1f}, Test Accuracy: {(100*test_res[-1]):>0.1f}")
    if save_model:
        if embeddings_or_features == 3:
            torch.save(model.state_dict(), dataset_fn[:-4]+"-both.pytorch-model")
        elif embeddings_or_features == 2:
            torch.save(model.state_dict(), dataset_fn[:-4]+"-features.pytorch-model")
        elif embeddings_or_features == 1:
            torch.save(model.state_dict(), dataset_fn[:-4]+"-embeddings.pytorch-model")
        else:
            torch.save(model.state_dict(), dataset_fn[:-4]+".pytorch-model")
    return {"train_result":train_res[-1],"test_result":test_res[-1], "targets_x": train_tss, "targets_y": test_tss}